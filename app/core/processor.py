#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import re
from datetime import datetime
from threading import Thread
from queue import Queue
from jinja2 import Environment
from jinja2 import FileSystemLoader
from models.site import Site
from models.reader import Reader
from models.report import Report
from models.comment import Comment
from helpers.hashing import md5
import json
from conf import config
import PyRSS2Gen
import markdown
import pika

logger = logging.getLogger(__name__)
queue = Queue()
proc = None
env = None

# store client IP in memory until classification 
client_ips = {}

class Processor(Thread):

    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        logger.info('processor thread started')
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
                elif msg['request'] == 'report':
                    report(msg['data'])
                elif msg['request'] == 'late_accept':
                    late_accept_comment(msg['data'])
                elif msg['request'] == 'late_reject':
                    late_reject_comment(msg['data'])
                else:
                    logger.info("throw unknown request " + str(msg))
            except:
                logger.exception("processing failure")


def new_comment(data):

    logger.info('new comment received: %s' % data)

    token = data.get('token', '')
    url = data.get('url', '')
    author_name = data.get('author', '').strip()
    author_email = data.get('email', '').strip()
    author_site = data.get('site', '').strip()
    message = data.get('message', '')
    subscribe = data.get('subscribe', '')
    clientip = data.get('clientip', '')

    # private mode: email contains gravar md5 hash
    if config.security['private']:
        author_gravatar = author_email
        author_email = ''
    else:
        author_gravatar = md5(author_email.lower())

    # create a new comment row
    site = Site.select().where(Site.token == token).get()

    if author_site and author_site[:4] != 'http':
        author_site = 'http://' + author_site

    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # add a row to Comment table
    comment = Comment(site=site, url=url, author_name=author_name,
                      author_site=author_site, author_email=author_email,
                      author_gravatar=author_gravatar,
                      content=message, created=created, published=None)
    comment.save()

    article_url = "http://" + site.url + url

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
        url=article_url, comment=comment_text)

    if clientip:
        client_ips[comment.ip] = clientip

    # send email
    subject = '%s: [%d:%s]' % (site.name, comment.id, token)
    mail(site.admin_email, subject, email_body)

    # Reader subscribes to further comments
    if not config.security['private'] and subscribe and author_email:
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
    if not m:
        logger.warn('ignore corrupted email. No token %s' % subject)
        return
    comment_id = int(m.group(1))
    token = m.group(2)

    # retrieve site and comment rows
    try:
        comment = Comment.select().where(Comment.id == comment_id).get()
    except:
        logger.warn('unknown comment %d' % comment_id)
        send_delete_command(data)
        return

    if comment.site.token != token:
        logger.warn('ignore corrupted email. Unknown token %d' % comment_id)
        return

    if not message:
        logger.warn('ignore empty email')
        return

    # accept email: request to delete
    send_delete_command(data)

    # safe logic: no answer or unknown answer is a go for publishing
    if message[:2].upper() in ('NO','SP'):

        # put a log to help fail2ban 
        if message[:2].upper() == 'SP': # SPAM
            if comment_id in client_ips:
                logger.info('SPAM comment from %s: %d' % (client_ips[comment_id], comment_id))
            else:
                logger.info('cannot identify SPAM source: %d' % comment_id)
            
        # forget client IP
        if comment_id in client_ips:
            del client_ips[comment_id]

        # report event
        report_rejected(comment)

        logger.info('discard comment: %d' % comment_id)
        comment.delete_instance()
        email_body = get_template('drop_comment').render(original=message)
        mail(from_email, 'Re: ' + subject, email_body)
    else:
        # report event
        report_published(comment)

        # update Comment row
        comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.save()
        logger.info('commit comment: %d' % comment_id)

        # rebuild RSS
        rss(token)

        # send approval confirmation email to admin
        email_body = get_template('approve_comment').render(original=message)
        mail(from_email, 'Re: ' + subject, email_body)

        # notify reader once comment is published
        if not config.security['private']:
            reader_email = get_email_metadata(message)
            if reader_email:
                notify_reader(from_email, reader_email, comment.site.token,
                              comment.site.url, comment.url)

            # notify subscribers every time a new comment is published
            notify_subscribed_readers(
                comment.site.token, comment.site.url, comment.url)


def late_reject_comment(id):

    # retrieve site and comment rows
    comment = Comment.select().where(Comment.id == id).get()

    # report event
    report_rejected(comment)

    # delete Comment row
    comment.delete_instance()

    logger.info('late reject comment: %s' % id)


def late_accept_comment(id):

    # retrieve site and comment rows
    comment = Comment.select().where(Comment.id == id).get()

    # report event
    report_published(comment)

    # update Comment row
    comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()

    logger.info('late accept comment: %s' % id)


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

        # report event
        report_subscribed(reader)


def unsubscribe_reader(data):
    token = data.get('token', '')
    url = data.get('url', '')
    email = data.get('email', '')
    logger.info('unsubscribe reader %s from %s (%s)' % (email, url, token))
    for reader in Reader.select().join(Site).where(Site.token == token,
                                                   Reader.email == email,
                                                   Reader.url == url):
        # report event
        report_unsubscribed(reader)

        reader.delete_instance()


def notify_subscribed_readers(token, site_url, url):
    logger.info('notify subscribers for %s (%s)' % (url, token))
    article_url = "http://" + site_url + url
    for reader in Reader.select().join(Site).where(Site.token == token,
                                                   Reader.url == url):
        to_email = reader.email
        logger.info('notify reader %s' % to_email)
        unsubscribe_url = '%s/unsubscribe?email=%s&token=%s&url=%s' % (
                          config.http['root_url'], to_email, token, reader.url)
        email_body = get_template(
            'notify_subscriber').render(article_url=article_url,
                                        unsubscribe_url=unsubscribe_url)
        subject = get_template('notify_message').render()
        mail(to_email, subject, email_body)


def notify_reader(from_email, to_email, token, site_url, url):
    logger.info('notify reader: email %s about URL %s' % (to_email, url))
    article_url = "http://" + site_url + url
    email_body = get_template('notify_reader').render(article_url=article_url)
    subject = get_template('notify_message').render()
    mail(to_email, subject, email_body)


def report_rejected(comment):
    report = Report(site=comment.site, url=comment.url,
                    name=comment.author_name, email=comment.author_email,
                    rejected=True)
    report.save()


def report_published(comment):
    report = Report(site=comment.site, url=comment.url,
                    name=comment.author_name, email=comment.author_email,
                    published=True)
    report.save()


def report_subscribed(reader):
    report = Report(site=reader.site, url=reader.url,
                    name='', email=reader.email,
                    subscribed=True)
    report.save()


def report_unsubscribed(reader):
    report = Report(site=reader.site, url=reader.url,
                    name='', email=reader.email,
                    unsubscribed=True)
    report.save()


def report(token):
    site = Site.select().where(Site.token == token).get()

    standbys = []
    for row in Comment.select().join(Site).where(
            Site.token == token, Comment.published.is_null(True)):
        standbys.append({'url': "http://" + site.url + row.url,
                         'created': row.created.strftime('%d/%m/%y %H:%M'),
                         'name': row.author_name, 'content': row.content,
                         'id': row.id})

    published = []
    for row in Report.select().join(Site).where(
            Site.token == token, Report.published):
        published.append({'url': "http://" + site.url + row.url,
                          'name': row.name, 'email': row.email})

    rejected = []
    for row in Report.select().join(Site).where(
            Site.token == token, Report.rejected):
        rejected.append({'url': "http://" + site.url + row.url,
                         'name': row.name, 'email': row.email})

    subscribed = []
    for row in Report.select().join(Site).where(
            Site.token == token, Report.subscribed):
        subscribed.append({'url': "http://" + site.url + row.url,
                           'name': row.name, 'email': row.email})

    unsubscribed = []
    for row in Report.select().join(Site).where(
            Site.token == token, Report.subscribed):
        unsubscribed.append({'url': "http://" + site.url + row.url,
                             'name': row.name, 'email': row.email})

    email_body = get_template('report').render(secret=config.security['secret'],
                                               root_url=config.http[
                                                   'root_url'],
                                               standbys=standbys,
                                               published=published,
                                               rejected=rejected,
                                               subscribed=subscribed,
                                               unsubscribed=unsubscribed)
    subject = get_template('report_message').render(site=site.name)

    mail(site.admin_email, subject, email_body)

    # delete report table
    Report.delete().execute()


def rss(token, onstart=False):

    if onstart and os.path.isfile(config.rss['file']):
        return

    site = Site.select().where(Site.token == token).get()
    rss_title = get_template('rss_title_message').render(site=site.name)
    md = markdown.Markdown()

    items = []
    for row in Comment.select().join(Site).where(
            Site.token == token, Comment.published).order_by(
                -Comment.published).limit(10):
        item_link = "%s://%s%s" % (config.rss['proto'], site.url, row.url)
        items.append(PyRSS2Gen.RSSItem(
            title='%s - %s://%s%s' % (config.rss['proto'],
                                      row.author_name, site.url, row.url),
            link=item_link,
            description=md.convert(row.content),
            guid=PyRSS2Gen.Guid('%s/%d' % (item_link, row.id)),
            pubDate=row.published
        ))

    rss = PyRSS2Gen.RSS2(
        title=rss_title,
        link='%s://%s' % (config.rss['proto'], site.url),
        description="Commentaires du site '%s'" % site.name,
        lastBuildDate=datetime.now(),
        items=items)
    rss.write_xml(open(config.rss['file'], 'w'), encoding='utf-8')


def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        config.rabbitmq['username'], config.rabbitmq['password'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                         'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))
    return connection


def mail(to_email, subject, message):

    body = {
        'to': to_email,
        'subject': subject,
        'content': message
    }
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.send',
                          body=json.dumps(body, indent=False, sort_keys=False))
    connection.close()
    logger.debug('Email for %s posted' % to_email)


def send_delete_command(content):

    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.basic_publish(exchange=config.rabbitmq['exchange'],
                          routing_key='mail.command.delete',
                          body=json.dumps(content, indent=False, sort_keys=False))
    connection.close()
    logger.debug('Email accepted. Delete request sent for %s' % content)


def get_template(name):
    return env.get_template(config.general['lang'] + '/' + name + '.tpl')


def enqueue(something):
    queue.put(something)


def get_processor():
    return proc


def start(template_dir):
    global proc, env

    # initialize Jinja 2 templating
    logger.info("load templates from directory %s" % template_dir)
    env = Environment(loader=FileSystemLoader(template_dir))

    # generate RSS for all sites
    for site in Site.select():
        rss(site.token, True)

    # start processor thread
    proc = Processor()
    proc.start()
