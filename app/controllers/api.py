#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, jsonify
from playhouse.shortcuts import model_to_dict
from app import app
from app.models.site import Site
from app.models.comment import Comment

logger = logging.getLogger(__name__)


@app.route("/comments", methods=['POST'])
def query_comments():

    query = request.json
    token = query['token']
    url = query['url']
    logger.info('token=%s url=%s' % (token, url))

    comments = []
    for comment in Comment.select(Comment).join(Site).where(
           (Comment.url == url) &
           (Site.token == token)).order_by(Comment.published):
        comments.append(model_to_dict(comment))

    r = jsonify({'data': comments})
    r.status_code = 200
    return r
