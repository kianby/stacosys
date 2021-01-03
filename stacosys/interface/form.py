#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from flask import abort, redirect, request

from stacosys.interface import app
from stacosys.model.comment import Comment
from stacosys.model.site import Site

logger = logging.getLogger(__name__)


@app.route("/newcomment", methods=["POST"])
def new_form_comment():

    try:
        data = request.form
        logger.info("form data " + str(data))

        # validate token: retrieve site entity
        token = data.get("token", "")
        site = Site.select().where(Site.token == token).get()
        if site is None:
            logger.warn("Unknown site %s" % token)
            abort(400)

        # honeypot for spammers
        captcha = data.get("remarque", "")
        if captcha:
            logger.warn("discard spam: data %s" % data)
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
            logger.warn("empty field: data %s" % data)
            abort(400)
        check_form_data(data)

        # add a row to Comment table
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment = Comment(
            site=site,
            url=url,
            author_name=author_name,
            author_site=author_site,
            author_gravatar=author_gravatar,
            content=message,
            created=created,
            notified=None,
            published=None,
        )
        comment.save()

    except:
        logger.exception("new comment failure")
        abort(400)

    return redirect("/redirect/", code=302)


def check_form_data(data):
    fields = ["url", "message", "site", "remarque", "author", "token", "email"]
    d = data.to_dict()
    for field in fields:
        if field in d:
            del d[field]
    if d:
        logger.warn("additional field: data %s" % data)
        abort(400)
