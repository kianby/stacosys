#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from flask import request, abort, redirect
from model.site import Site
from model.comment import Comment
from conf import config
from helper.hashing import md5

logger = logging.getLogger(__name__)
app = config.flaskapp()

@app.route("/newcomment", methods=["POST"])
def new_form_comment():

    try:
        data = request.form

        # add client IP if provided by HTTP proxy
        ip = ""
        if "X-Forwarded-For" in request.headers:
            ip = request.headers["X-Forwarded-For"]

        # log
        logger.info(data)

        # validate token: retrieve site entity
        token = data.get("token", "")
        site = Site.select().where(Site.token == token).get()
        if site is None:
            logger.warn("Unknown site %s" % token)
            abort(400)

        # honeypot for spammers
        captcha = data.get("captcha", "")
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

        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # add a row to Comment table
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
            ip=ip,
        )
        comment.save()

    except:
        logger.exception("new comment failure")
        abort(400)

    return redirect("/redirect/", code=302)
