#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from datetime import datetime
from threading import Thread
from queue import Queue
from jinja2 import Environment, FileSystemLoader
from app.models.site import Site
from app.models.comment import Comment
from app.models.reader import Reader
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
                elif msg['request'] == 'unsubscribe':
                    unsubscribe_reader(msg['data'])
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
    email_body = get_template('new_comment').render(
        url=url, comment=comment_text)

    # send email
    subject = '%s: [%d:%s]' % (site.name, comment.id, token)
    mail(site.admin_email, subject, email_body)

    # Reader subscribes to further comments
    if subscribe and author_email:
        subscribe_reader(author_email, token, url)

    logger.debug("new comment processed ")


def reply_comment_email(data):

    from_email = data['from']
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

    if not message:
        logger.warn('ignore empty email')
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if message[:2].upper() == 'NO':
        logger.info('discard comment: %d' % comment_id)
        comment.delete_instance()
        email_body = get_template('drop_comment').render(original=message)
        mail(from_email, 'Re: ' + subject, email_body)
    else:
        # update Comment row
        comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.save()

        logger.info('commit comment: %d' % comment_id)

        # send approval confirmation email to admin
        email_body = get_template('approve_comment').render(original=message)
        mail(from_email, 'Re: ' + subject, email_body)

        # notify reader once comment is published
        reader_email = get_email_metadata(message)
        if reader_email:
            notify_reader(from_email, reader_email, comment.site.token,
                          comment.url)

        # notify subscribers every time a new comment is published
        notify_subscribed_readers(comment.site.token, comment.url)


def get_email_metadata(message):
    # retrieve metadata reader email from email body sent by admin
    email = ""
    m = re.search('email:\s(.+@.+\..+)', message)
    if m:
        email = m.group(1)
    return email


def subscribe_reader(email, token, url):
    logger.info('subscribe reader %s to %s [%s]' % (email, url, token))
    recorded = Reader.select().join(Site).where(Site.token == token,
                                                Reader.email == email,
                                                Reader.url == url).count()
    if recorded:
        logger.debug('reader %s is already recorded' % email)
    else:
        site = Site.select().where(Site.token == token).get()
        reader = Reader(site=site, email=email, url=url)
        reader.save()


def unsubscribe_reader(data):
    token = data.get('token', '')
    url = data.get('url', '')
    email = data.get('email', '')
    logger.info('unsubscribe reader %s from %s (%s)' % (email, url, token))
    for reader in Reader.select().join(Site).where(Site.token == token,
                                                   Reader.email == email,
                                                   Reader.url == url):
        reader.delete_instance()


def notify_subscribed_readers(token, url):
    logger.info('notify subscribers for %s (%s)' % (url, token))
    for reader in Reader.select().join(Site).where(Site.token == token,
                                                   Reader.url == url):
        to_email = reader.email
        logger.info('notify reader %s' % to_email)
        unsubscribe_url = '%s?email=%s&token=%s&url=%s' % (
                          config.UNSUBSCRIBE_URL, to_email, token, reader.url)
        email_body = get_template(
            'notify_subscriber').render(article_url=reader.url,
                                        unsubscribe_url=unsubscribe_url)
        subject = get_template('notify_message').render()
        mail(to_email, subject, email_body)


def notify_reader(from_email, to_email, token, url):
    logger.info('notify reader: email %s about URL %s' % (to_email, url))
    email_body = get_template('notify_reader').render(article_url=url)
    subject = get_template('notify_message').render()
    mail(to_email, subject, email_body)


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
