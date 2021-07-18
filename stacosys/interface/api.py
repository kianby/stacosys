#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask import jsonify, request

from stacosys.db import dao
from stacosys.interface import app

logger = logging.getLogger(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    return "OK"


@app.route("/comments", methods=["GET"])
def query_comments():
    comments = []
    url = request.args.get("url", "")

    logger.info("retrieve comments for url %s" % url)
    for comment in dao.find_published_comments_by_url(url):
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
    return jsonify({"data": comments})


@app.route("/comments/count", methods=["GET"])
def get_comments_count():
    url = request.args.get("url", "")
    return jsonify({"count": dao.count_published_comments(url)})
