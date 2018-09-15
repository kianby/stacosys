#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from core import mailer
from core import templater
from model.comment import Comment
from model.comment import Site

logger = logging.getLogger(__name__)


def fetch_mail_answers():

    logger.info("DEBUT POP MAIL")
    time.sleep(80)
    logger.info("FIN POP MAIL")
    # data = request.get_json()
    # logger.debug(data)

    # processor.enqueue({'request': 'new_mail', 'data': data})


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
        email_body = templater.get_template("new_comment").render(url=comment.url, comment=comment_text)

        site = Site.select().where(Site.id == Comment.site).get()
        # send email
        subject = "STACOSYS %s: [%d:%s]" % (site.name, comment.id, site.token)
        mailer.send_mail(site.admin_email, subject, email_body)
        logger.debug("new comment processed ")
