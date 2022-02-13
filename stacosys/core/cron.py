#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from stacosys.db import dao

logger = logging.getLogger(__name__)


def submit_new_comment(site_name, site_admin_email, mailer):
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
        email_body = "\n".join(comment_list)

        # send email to notify admin
        subject = "STACOSYS %s" % site_name
        if mailer.send(site_admin_email, subject, email_body):
            logger.debug("new comment processed ")

            # save notification datetime
            dao.notify_comment(comment)
        else:
            logger.warning("rescheduled. send mail failure " + subject)
