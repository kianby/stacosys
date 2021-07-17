#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re

from stacosys.core.templater import Templater, Template
from stacosys.model.comment import Comment
from stacosys.model.email import Email
from stacosys.core.rss import Rss
from stacosys.core.mailer import Mailer
from stacosys.db import dao

logger = logging.getLogger(__name__)

current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
templater = Templater(template_path)


def fetch_mail_answers(lang, mailer: Mailer, rss: Rss, site_token):
    for msg in mailer.fetch():
        if re.search(r".*STACOSYS.*\[(\d+)\:(\w+)\]", msg.subject, re.DOTALL):
            if _reply_comment_email(lang, mailer, rss, msg, site_token):
                mailer.delete(msg.id)


def _reply_comment_email(lang, mailer: Mailer, rss: Rss, email: Email, site_token):

    m = re.search(r"\[(\d+)\:(\w+)\]", email.subject)
    if not m:
        logger.warning("ignore corrupted email. No token %s" % email.subject)
        return
    comment_id = int(m.group(1))
    token = m.group(2)
    if token != site_token:
        logger.warning("ignore corrupted email. Unknown token %d" % comment_id)
        return

    # retrieve site and comment rows
    comment = Comment
    if not comment:
        logger.warning("unknown comment %d" % comment_id)
        return True

    if comment.published:
        logger.warning("ignore already published email. token %d" % comment_id)
        return

    if not email.plain_text_content:
        logger.warning("ignore empty email")
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if email.plain_text_content[:2].upper() == "NO":
        logger.info("discard comment: %d" % comment_id)
        comment.delete_instance()
        new_email_body = templater.get_template(lang, Template.DROP_COMMENT).render(
            original=email.plain_text_content
        )
        if not mailer.send(email.from_addr, "Re: " + email.subject, new_email_body):
            logger.warning("minor failure. cannot send rejection mail " + email.subject)
    else:
        # save publishing datetime
        dao.publish(comment)
        logger.info("commit comment: %d" % comment_id)

        # rebuild RSS
        rss.generate()

        # send approval confirmation email to admin
        new_email_body = templater.get_template(lang, Template.APPROVE_COMMENT).render(
            original=email.plain_text_content
        )
        if not mailer.send(email.from_addr, "Re: " + email.subject, new_email_body):
            logger.warning("minor failure. cannot send approval email " + email.subject)

    return True


def submit_new_comment(lang, site_name, site_token, site_admin_email, mailer):
    for comment in Comment.select().where(Comment.notified.is_null()):
        comment_list = (
            "author: %s" % comment.author_name,
            "site: %s" % comment.author_site,
            "date: %s" % comment.created,
            "url: %s" % comment.url,
            "",
            "%s" % comment.content,
            "",
        )
        comment_text = "\n".join(comment_list)
        email_body = templater.get_template(lang, Template.NEW_COMMENT).render(
            url=comment.url, comment=comment_text
        )

        # send email
        subject = "STACOSYS %s: [%d:%s]" % (site_name, comment.id, site_token)
        if mailer.send(site_admin_email, subject, email_body):
            logger.debug("new comment processed ")

            # notify site admin and save notification datetime
            dao.notify_site_admin(comment)
        else:
            logger.warning("rescheduled. send mail failure " + subject)
