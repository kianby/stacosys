#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import re
import PyRSS2Gen
import markdown
import json
from datetime import datetime
from threading import Thread
from queue import Queue
from jinja2 import Environment
from jinja2 import FileSystemLoader
from models.site import Site
from models.comment import Comment
from helpers.hashing import md5
from conf import config
from core import mailer


logger = logging.getLogger(__name__)
queue = Queue()
proc = None
env = None

# keep client IP in memory until classified
client_ips = {}


class Processor(Thread):
    def stop(self):
        logger.info("stop requested")
        self.is_running = False

    def run(self):

        logger.info("processor thread started")
        self.is_running = True
        while self.is_running:
            try:
                msg = queue.get()
                if msg["request"] == "new_mail":
                    reply_comment_email(msg["data"])
                    send_delete_command(msg["data"])
                else:
                    logger.info("throw unknown request " + str(msg))
            except:
                logger.exception("processing failure")


def reply_comment_email(data):

    from_email = data["from"]
    subject = data["subject"]
    message = ""
    for part in data["parts"]:
        if part["content-type"] == "text/plain":
            message = part["content"]
            break

    m = re.search("\[(\d+)\:(\w+)\]", subject)
    if not m:
        logger.warn("ignore corrupted email. No token %s" % subject)
        return
    comment_id = int(m.group(1))
    token = m.group(2)

    # retrieve site and comment rows
    try:
        comment = Comment.select().where(Comment.id == comment_id).get()
    except:
        logger.warn("unknown comment %d" % comment_id)
        return

    if comment.published:
        logger.warn("ignore already published email. token %d" % comment_id)
        return

    if comment.site.token != token:
        logger.warn("ignore corrupted email. Unknown token %d" % comment_id)
        return

    if not message:
        logger.warn("ignore empty email")
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if message[:2].upper() in ("NO", "SP"):

        # put a log to help fail2ban
        if message[:2].upper() == "SP":  # SPAM
            if comment_id in client_ips:
                logger.info(
                    "SPAM comment from %s: %d" % (client_ips[comment_id], comment_id)
                )
            else:
                logger.info("cannot identify SPAM source: %d" % comment_id)

        # forget client IP
        if comment_id in client_ips:
            del client_ips[comment_id]

        logger.info("discard comment: %d" % comment_id)
        comment.delete_instance()
        email_body = get_template("drop_comment").render(original=message)
        mail(from_email, "Re: " + subject, email_body)
    else:
        # update Comment row
        comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.save()
        logger.info("commit comment: %d" % comment_id)

        # rebuild RSS
        rss(token)

        # send approval confirmation email to admin
        email_body = get_template("approve_comment").render(original=message)
        mail(from_email, "Re: " + subject, email_body)


def get_email_metadata(message):
    # retrieve metadata reader email from email body sent by admin
    email = ""
    m = re.search(r"email:\s(.+@.+\..+)", message)
    if m:
        email = m.group(1)
    return email


def rss(token, onstart=False):

    if onstart and os.path.isfile(config.rss["file"]):
        return

    site = Site.select().where(Site.token == token).get()
    rss_title = get_template("rss_title_message").render(site=site.name)
    md = markdown.Markdown()

    items = []
    for row in (
        Comment.select()
        .join(Site)
        .where(Site.token == token, Comment.published)
        .order_by(-Comment.published)
        .limit(10)
    ):
        item_link = "%s://%s%s" % (config.rss["proto"], site.url, row.url)
        items.append(
            PyRSS2Gen.RSSItem(
                title="%s - %s://%s%s"
                % (config.rss["proto"], row.author_name, site.url, row.url),
                link=item_link,
                description=md.convert(row.content),
                guid=PyRSS2Gen.Guid("%s/%d" % (item_link, row.id)),
                pubDate=row.published,
            )
        )

    rss = PyRSS2Gen.RSS2(
        title=rss_title,
        link="%s://%s" % (config.rss["proto"], site.url),
        description="Commentaires du site '%s'" % site.name,
        lastBuildDate=datetime.now(),
        items=items,
    )
    rss.write_xml(open(config.rss["file"], "w"), encoding="utf-8")


def send_delete_command(content):
    # TODO delete mail
    pass


def get_template(name):
    return env.get_template(config.general["lang"] + "/" + name + ".tpl")


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
