#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask import abort, jsonify, request

from stacosys.conf import config
from stacosys.model.comment import Comment
from stacosys.model.site import Site

logger = logging.getLogger(__name__)
app = config.flaskapp()


@app.route('/ping', methods=['GET'])
def ping():
    return 'OK'


@app.route('/comments', methods=['GET'])
def query_comments():

    comments = []
    try:
        token = request.args.get('token', '')
        url = request.args.get('url', '')

        logger.info('retrieve comments for url %s' % (url))
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
            d = {
                'author': comment.author_name,
                'content': comment.content,
                'avatar': comment.author_gravatar,
                'date': comment.published.strftime('%Y-%m-%d %H:%M:%S') 
            }
            if comment.author_site:
                d['site'] = comment.author_site
            logger.debug(d)
            comments.append(d)
        r = jsonify({'data': comments})
        r.status_code = 200
    except:
        logger.warn('bad request')
        r = jsonify({'data': []})
        r.status_code = 400
    return r


@app.route('/comments/count', methods=['GET'])
def get_comments_count():
    try:
        token = request.args.get('token', '')
        url = request.args.get('url', '')
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
        r = jsonify({'count': count})
        r.status_code = 200
    except:
        r = jsonify({'count': 0})
        r.status_code = 200
    return r
