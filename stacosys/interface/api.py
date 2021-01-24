#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import abort, jsonify, request

from stacosys.interface import app
from stacosys.model.comment import Comment

logger = logging.getLogger(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return "OK"


@app.route("/comments", methods=["GET"])
def query_comments():

    comments = []
    try:
        token = request.args.get("token", "")
        if token != app.config.get("SITE_TOKEN"):
            abort(401)

        url = request.args.get("url", "")

        logger.info("retrieve comments for url %s" % (url))
        for comment in (
            Comment.select(Comment)
            .where((Comment.url == url) & (Comment.published.is_null(False)))
            .order_by(+Comment.published)
        ):
            d = {
                "author": comment.author_name,
                "content": comment.content,
                "avatar": comment.author_gravatar,
                "date": comment.published.strftime("%Y-%m-%d %H:%M:%S"),
            }
            if comment.author_site:
                d["site"] = comment.author_site
            logger.debug(d)
            comments.append(d)
        r = jsonify({"data": comments})
        r.status_code = 200
    except Exception:
        logger.warn("bad request")
        r = jsonify({"data": []})
        r.status_code = 400
    return r


@app.route("/comments/count", methods=["GET"])
def get_comments_count():
    try:
        token = request.args.get("token", "")
        if token != app.config.get("SITE_TOKEN"):
            abort(401)

        url = request.args.get("url", "")
        count = (
            Comment.select(Comment)
            .where((Comment.url == url) & (Comment.published.is_null(False)))
            .count()
        )
        r = jsonify({"count": count})
        r.status_code = 200
    except Exception:
        r = jsonify({"count": 0})
        r.status_code = 200
    return r
