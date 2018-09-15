#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
import time
import re
from core import mailer
from core.templater import get_template
from core import rss
from model.comment import Comment
from model.comment import Site

logger = logging.getLogger(__name__)


def cron(func):
    def wrapper():
        logger.debug("execute CRON " + func.__name__)
        func()

    return wrapper


@cron
def fetch_mail_answers():

    for msg in mailer.fetch():
        m = re.search(r"\[(\d+)\:(\w+)\]", msg["subject"])
        if m:
            full_msg = mailer.get(msg["id"])
            if full_msg:
                reply_comment_email(full_msg)
                mailer.delete(msg["id"])


@cron
def submit_new_comment():

    for comment in Comment.select().where(Comment.notified.is_null()):

        comment_list = (
            "author: %s" % comment.author_name,
            "site: %s" % comment.author_site,
            "date: %s" % comment.create,
            "url: %s" % comment.url,
            "",
            "%s" % comment.message,
            "",
        )
        comment_text = "\n".join(comment_list)
        email_body = get_template("new_comment").render(
            url=comment.url, comment=comment_text
        )

        # send email
        site = Site.select().where(Site.id == Comment.site).get()
        subject = "STACOSYS %s: [%d:%s]" % (site.name, comment.id, site.token)
        mailer.send(site.admin_email, subject, email_body)
        logger.debug("new comment processed ")


def reply_comment_email(data):

    from_email = data["from"]
    subject = data["subject"]
    message = ""
    for part in data["parts"]:
        if part["content-type"] == "text/plain":
            message = part["content"]
            break

    m = re.search(r"\[(\d+)\:(\w+)\]", subject)
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
            if comment.ip:
                logger.info(
                    "SPAM comment from %s: %d" % (client_ips[comment_id], comment_id)
                )
            else:
                logger.info("cannot identify SPAM source: %d" % comment_id)

        logger.info("discard comment: %d" % comment_id)
        comment.delete_instance()
        email_body = get_template("drop_comment").render(original=message)
        mailer.send(from_email, "Re: " + subject, email_body)
    else:
        # update Comment row
        comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.ip = None
        comment.save()
        logger.info("commit comment: %d" % comment_id)

        # rebuild RSS
        rss.generate_site(token)

        # send approval confirmation email to admin
        email_body = get_template("approve_comment").render(original=message)
        mailer.send(from_email, "Re: " + subject, email_body)

