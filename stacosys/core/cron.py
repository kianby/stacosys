#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import re

from stacosys.core.mailer import Mailer
from stacosys.core.rss import Rss
from stacosys.core.templater import Templater, Template
from stacosys.db import dao
from stacosys.model.email import Email

REGEX_EMAIL_SUBJECT = r".*STACOSYS.*\[(\d+)\:(\w+)\]"

logger = logging.getLogger(__name__)

current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
templater = Templater(template_path)


def fetch_mail_answers(lang, mailer: Mailer, rss: Rss, site_token):
    while True:
        msgs = mailer.fetch()
        if len(msgs) == 0:
            break
        msg = msgs[0]
        _process_answer_msg(msg, lang, mailer, rss, site_token)
        mailer.delete(msg.id)


def _process_answer_msg(msg, lang, mailer: Mailer, rss: Rss, site_token):
    # filter stacosys e-mails
    m = re.search(REGEX_EMAIL_SUBJECT, msg.subject, re.DOTALL)
    if not m:
        return

    comment_id = int(m.group(1))
    submitted_token = m.group(2)

    # validate token
    if submitted_token != site_token:
        logger.warning("ignore corrupted email. Unknown token %d" % comment_id)
        return

    if not msg.plain_text_content:
        logger.warning("ignore empty email")
        return

    _reply_comment_email(lang, mailer, rss, msg, comment_id)


def _reply_comment_email(lang, mailer: Mailer, rss: Rss, email: Email, comment_id):
    # retrieve comment
    comment = dao.find_comment_by_id(comment_id)
    if not comment:
        logger.warning("unknown comment %d" % comment_id)
        return

    if comment.published:
        logger.warning("ignore already published email. token %d" % comment_id)
        return

    # safe logic: no answer or unknown answer is a go for publishing
    if email.plain_text_content[:2].upper() == "NO":
        logger.info("discard comment: %d" % comment_id)
        dao.delete_comment(comment)
        new_email_body = templater.get_template(lang, Template.DROP_COMMENT).render(
            original=email.plain_text_content
        )
        if not mailer.send(email.from_addr, "Re: " + email.subject, new_email_body):
            logger.warning("minor failure. cannot send rejection mail " + email.subject)
    else:
        # save publishing datetime
        dao.publish_comment(comment)
        logger.info("commit comment: %d" % comment_id)

        # rebuild RSS
        rss.generate()

        # send approval confirmation email to admin
        new_email_body = templater.get_template(lang, Template.APPROVE_COMMENT).render(
            original=email.plain_text_content
        )
        if not mailer.send(email.from_addr, "Re: " + email.subject, new_email_body):
            logger.warning("minor failure. cannot send approval email " + email.subject)


def submit_new_comment(lang, site_name, site_token, site_admin_email, mailer):
    for comment in dao.find_not_notified_comments():
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

        # send email to notify admin
        subject = "STACOSYS %s: [%d:%s]" % (site_name, comment.id, site_token)
        if mailer.send(site_admin_email, subject, email_body):
            logger.debug("new comment processed ")

            # save notification datetime
            dao.notify_comment(comment)
        else:
            logger.warning("rescheduled. send mail failure " + subject)
