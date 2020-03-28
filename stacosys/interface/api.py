#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, jsonify, abort
from model.site import Site
from model.comment import Comment
from conf import config

logger = logging.getLogger(__name__)
app = config.flaskapp()


@app.route("/ping", methods=["GET"])
def ping():
    return "OK"


@app.route("/comments", methods=["GET"])
def query_comments():

    comments = []
    try:
        token = request.args.get("token", "")
        url = request.args.get("url", "")

        logger.info("retrieve comments for token %s, url %s" % (token, url))
        for comment in (
            Comment.select(Comment)
            .join(Site)
            .where(
                (Comment.url == url)
                & (Comment.published.is_null(False))
                & (Site.token == token)
            )
            .order_by(+Comment.published)
        ):
            d = {}
            d["author"] = comment.author_name
            d["content"] = comment.content
            if comment.author_site:
                d["site"] = comment.author_site
            d["avatar"] = comment.author_gravatar
            d["date"] = comment.published.strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(d)
            comments.append(d)
        r = jsonify({"data": comments})
        r.status_code = 200
    except:
        logger.warn("bad request")
        r = jsonify({"data": []})
        r.status_code = 400
    return r


@app.route("/comments/count", methods=["GET"])
def get_comments_count():
    try:
        token = request.args.get("token", "")
        url = request.args.get("url", "")
        count = (
            Comment.select(Comment)
            .join(Site)
            .where(
                (Comment.url == url)
                & (Comment.published.is_null(False))
                & (Site.token == token)
            )
            .count()
        )
        r = jsonify({"count": count})
        r.status_code = 200
    except:
        r = jsonify({"count": 0})
        r.status_code = 200
    return r
