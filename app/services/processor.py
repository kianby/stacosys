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
import requests
import json
import config


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
            try:
                msg = queue.get()
                if msg['request'] == 'new_comment':
                    new_comment(msg['data'])
                elif msg['request'] == 'new_mail':
                    reply_comment_email(msg['data'])
                #elif req['type'] == 'unsubscribe':
                #    unsubscribe_reader(req['email'], req['article'])
                else:
                    logger.info("throw unknown request " + str(msg))
            except:
                logger.exception("processing failure")


def new_comment(data):

    logger.info('new comment received: %s' % data)

    token = data.get('token', '')
    url = data.get('url', '')
    author_name = data.get('author', '')
    author_email = data.get('email', '')
    author_site = data.get('site', '')
    message = data.get('message', '')
    subscribe = data.get('subscribe', '')

    # create a new comment row
    site = Site.select().where(Site.token == token).get()

    if author_site and author_site[:4] != 'http':
        author_site = 'http://' + author_site

    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # add a row to Comment table
    comment = Comment(site=site, url=url, author_name=author_name,
            author_site=author_site, author_email=author_email,
            content=message, created=created, published=None)
    comment.save()

    # render email body template
    comment_list = (
        'author: %s' % author_name,
        'email: %s' % author_email,
        'site: %s' % author_site,
        'date: %s' % created,
        'url: %s' % url,
        '',
        '%s' % message,
        ''
    )
    comment_text = '\n'.join(comment_list)
    email_body = get_template('new_comment').render(url=url, comment=comment_text)

    # send email
    # TODO subject should embed a key 
    subject = '%s: [%d:%s]' % (site.name, comment.id, token)
    mail(site.admin_email, subject, email_body)

    # TODO support subscription
    # Reader subscribes to further comments
    #if subscribe and email:
    #    subscribe_reader(email, article, url)

    logger.debug("new comment processed ")


def reply_comment_email(data):

    email_address = data['from']
    subject = data['subject']
    message = ''
    for part in data['parts']:
        if part['content-type'] == 'text/plain':
            message = part['content']
            break

    m = re.search('\[(\d+)\:(\w+)\]', subject)
    comment_id = int(m.group(1))
    token = m.group(2)

    # retrieve site and comment rows
    comment = Comment.select().where(Comment.id == comment_id).get()
    if comment.site.token != token:
        logger.warn('ignore corrupted email')
        return

    # TODO validate chardet decoding is no more needed
    #message = decode_best_effort(message)
    if not message:
        logger.warn('ignore empty email')
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if message[:2].upper() == 'NO':
        logger.info('discard comment: %d' % comment_id)
        comment.delete_instance()
        email_body = get_template('drop_comment').render(original=message)
        mail(email_address, 'Re: ' + subject, email_body)
    else:
        # update Comment row 
        comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.save()

        logger.info('commit comment: %d' % comment_id)

        # send approval confirmation email to admin
        email_body = get_template('approve_comment').render(original=message)
        mail(email_address, 'Re: ' + subject, email_body)

        # TODO manage subscriptions
        # notify reader once comment is published
        #reader_email, article_url = get_email_metadata(message)
        #if reader_email:
        #    notify_reader(reader_email, article_url)

        # notify subscribers every time a new comment is published
        #notify_subscribers(article)


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


def mail(to_email, subject, message):

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    msg = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    r = requests.post(config.MAIL_URL, data=json.dumps(msg), headers=headers)
    if r.status_code in (200, 201):
        logger.debug('Email for %s posted' % to_email)
    else:
        logger.warn('Cannot post email for %s' % to_email)


def get_template(name):
    return env.get_template(config.LANG + '/' + name + '.tpl')


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
