#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from datetime import datetime
from threading import Thread
from queue import Queue
import chardet
from jinja2 import Environment, FileSystemLoader
from app.models.site import Site
from app.models.comment import Comment


logger = logging.getLogger(__name__)
queue = Queue()
proc = None
env = None


class Processor(Thread):

    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        self.is_running = True
        while self.is_running:
            msg = queue.get()
            if msg['request'] == 'new_comment':
                new_comment(msg['data'])
            #elif msg['type'] == 'reply_comment_email':
            #    reply_comment_email(req['From'], req['Subject'], req['Body'])
            #elif req['type'] == 'unsubscribe':
            #    unsubscribe_reader(req['email'], req['article'])
            else:
                logger.info("Dequeue unknown request " + str(msg))


def new_comment(data):

    try:
        token = data.get('token', '')
        url = data.get('url', '')
        author_name = data.get('author', '')
        author_email = data.get('email', '')
        author_site = data.get('site', '')
        message = data.get('message', '')
        subscribe = data.get('subscribe', '')

        # create a new comment row
        site = Site.select().where(Site.token == token).get()
        
        logger.info('new comment received: %s' % data)

        if author_site and author_site[:4] != 'http':
            author_site = 'http://' + author_site

        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        comment = Comment(site=site, url=url, author_name=author_name,
                author_site=author_site, author_email=author_email,
                content=message, created=created, published=None)
        comment.save()

        1 / 0 
        # Render email body template
        email_body = get_template('new_comment').render(url=url, comment=comment)

        # Send email
        mail(pecosys.get_config('post', 'from_email'),
             pecosys.get_config('post', 'to_email'),
             '[' + branch_name + '-' + article + ']',  email_body)

        # Reader subscribes to further comments
        if subscribe and email:
            subscribe_reader(email, article, url)

        logger.debug("new comment processed ")
    except:
        logger.exception("new_comment failure")


def reply_comment_email(from_email, subject, message):
    try:
        m = re.search('\[(\d+)\-(\w+)\]', subject)
        branch_name = m.group(1)
        article = m.group(2)

        message = decode_best_effort(message)

        # safe logic: no answer or unknown answer is a go for publishing
        if message[:2].upper() == 'NO':
            logger.info('discard comment: %s' % branch_name)
            email_body = get_template('drop_comment').render(original=message)
            mail(pecosys.get_config('post', 'from_email'),
                 pecosys.get_config('post', 'to_email'),
                 'Re: ' + subject, email_body)
        else:
            if pecosys.get_config("git", "disabled"):
                logger.debug("GIT usage disabled (debug mode)")
            else:
                git.merge(branch_name)
                if pecosys.get_config("git", "remote"):
                    git.push()
                logger.info('commit comment: %s' % branch_name)

            # send approval confirmation email to admin
            email_body = get_template('approve_comment').render(original=message)
            mail(pecosys.get_config('post', 'from_email'),
                 pecosys.get_config('post', 'to_email'),
                 'Re: ' + subject, email_body)

            # notify reader once comment is published
            reader_email, article_url = get_email_metadata(message)
            if reader_email:
                notify_reader(reader_email, article_url)

            # notify subscribers every time a new comment is published
            notify_subscribers(article)

        if pecosys.get_config("git", "disabled"):
            logger.debug("GIT usage disabled (debug mode)")
        else:
            git.branch("-D", branch_name)
    except:
        logger.exception("new email failure")


def get_email_metadata(message):
    # retrieve metadata reader email and URL from email body sent by admin
    email = ""
    url = ""
    m = re.search('email:\s(.+@.+\..+)', message)
    if m:
        email = m.group(1)

    m = re.search('url:\s(.+)', message)
    if m:
        url = m.group(1)
    return (email, url)


def subscribe_reader(email, article, url):
    logger.info("subscribe reader %s to %s (%s)" % (email, article, url))
    db = TinyDB(pecosys.get_config('global', 'cwd') + '/db.json')
    db.insert({'email': email, 'article': article, 'url': url})


def unsubscribe_reader(email, article):
    logger.info("unsubscribe reader %s from %s" % (email, article))
    db = TinyDB(pecosys.get_config('global', 'cwd') + '/db.json')
    db.remove((where('email') == email) & (where('article') == article))


def notify_subscribers(article):
    logger.info('notify subscribers for article %s' % article)
    db = TinyDB(pecosys.get_config('global', 'cwd') + '/db.json')
    for item in db.search(where('article') == article):
        logger.info(item)
        to_email = item['email']
        logger.info("notify reader %s for article %s" % (to_email, article))
        unsubscribe_url = pecosys.get_config('subscription', 'url') + '?email=' + to_email + '&article=' + article
        email_body = get_template('notify_subscriber').render(article_url=item['url'],
                                                              unsubscribe_url=unsubscribe_url)
        subject = get_template('notify_message').render()
        mail(pecosys.get_config('subscription', 'from_email'), to_email, subject, email_body)


def notify_reader(email, url):
    logger.info('notify reader: email %s about URL %s' % (email, url))
    email_body = get_template('notify_reader').render(article_url=url)
    subject = get_template('notify_message').render()
    mail(pecosys.get_config('subscription', 'from_email'), email, subject, email_body)


def decode_best_effort(string):
    info = chardet.detect(string)
    if info['confidence'] < 0.5:
        return string.decode('utf8', errors='replace')
    else:
        return string.decode(info['encoding'], errors='replace')


def mail(from_email, to_email, subject, *messages):

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.preamble = subject

    for message in messages:
        part = MIMEText(message, 'plain')
        msg.attach(part)

    s = smtplib.SMTP(pecosys.get_config('smtp', 'host'),
                     pecosys.get_config('smtp', 'port'))
    if(pecosys.get_config('smtp', 'starttls')):
        s.starttls()
    s.login(pecosys.get_config('smtp', 'login'),
            pecosys.get_config('smtp', 'password'))
    s.sendmail(from_email, to_email, msg.as_string())
    s.quit()


def get_template(name):
    return env.get_template(pecosys.get_config('global', 'lang') + '/' + name + '.tpl')


def enqueue(something):
    queue.put(something)


def get_processor():
    return proc


def start(template_dir):
    global proc, env

    # initialize Jinja 2 templating
    logger.info("load templates from directory %s" % template_dir)
    env = Environment(loader=FileSystemLoader(template_dir))

    # start processor thread
    proc = Processor()
    proc.start()
