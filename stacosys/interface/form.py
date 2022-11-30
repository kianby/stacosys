#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import abort, redirect, request

from stacosys.db import dao
from stacosys.interface import app, submit_new_comment
from stacosys.service import config
from stacosys.service.configuration import ConfigParameter

logger = logging.getLogger(__name__)


@app.route("/newcomment", methods=["POST"])
def new_form_comment():
    data = request.form
    logger.info("form data %s", str(data))

    # honeypot for spammers
    captcha = data.get("remarque", "")
    if captcha:
        logger.warning("discard spam: data %s", data)
        abort(400)

    url = data.get("url", "")
    author_name = data.get("author", "").strip()
    author_gravatar = data.get("email", "").strip()
    author_site = data.get("site", "").lower().strip()
    if author_site and author_site[:4] != "http":
        author_site = "http://" + author_site
    message = data.get("message", "")

    # anti-spam again
    if not url or not author_name or not message:
        logger.warning("empty field: data %s", data)
        abort(400)
    if not check_form_data(data.to_dict()):
        logger.warning("additional field: data %s", data)
        abort(400)

    # add a row to Comment table
    comment = dao.create_comment(
        url, author_name, author_site, author_gravatar, message
    )

    # send notification e-mail asynchronously
    submit_new_comment(comment)

    return redirect(config.get(ConfigParameter.SITE_REDIRECT), code=302)


def check_form_data(posted_comment):
    fields = ["url", "message", "site", "remarque", "author", "token", "email"]
    filtered = dict(filter(lambda x: x[0] not in fields, posted_comment.items()))
    return not filtered
