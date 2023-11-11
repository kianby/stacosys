#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import background
from flask import Flask

from stacosys.db import dao
from stacosys.service import config, mailer
from stacosys.service.configuration import ConfigParameter

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

logger = logging.getLogger(__name__)


@background.task
def submit_new_comment(comment):
    site_url = config.get(ConfigParameter.SITE_URL)
    comment_list = (
        f"Web admin interface: {site_url}/web/admin",
        "",
        f"author: {comment.author_name}",
        f"site: {comment.author_site}",
        f"date: {comment.created}",
        f"url: {comment.url}",
        "",
        comment.content,
        "",
    )
    email_body = "\n".join(comment_list)

    # send email to notify admin
    site_name = config.get(ConfigParameter.SITE_NAME)
    subject = f"STACOSYS {site_name}"
    if mailer.send(subject, email_body):
        logger.debug("new comment processed")
        # save notification datetime
        dao.notify_comment(comment)
