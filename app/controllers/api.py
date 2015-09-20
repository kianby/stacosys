#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import config
from flask import request, jsonify, abort
from app import app
from app.models.site import Site
from app.models.comment import Comment
from app.helpers.hashing import md5
from app.services import processor

logger = logging.getLogger(__name__)


@app.route("/comments", methods=['GET'])
def query_comments():

    comments = []
    try:
        token = request.args.get('token', '')
        url = request.args.get('url', '')

        logger.info('retrieve comments for token %s, url %s' % (token, url))
        for comment in Comment.select(Comment).join(Site).where(
                (Comment.url == url) &
                (Comment.published.is_null(False)) &
                (Site.token == token)).order_by(+Comment.published):
            d = {}
            d['author'] = comment.author_name
            d['content'] = comment.content
            if comment.author_site:
                d['site'] = comment.author_site
            if comment.author_email:
                d['avatar'] = md5(comment.author_email.strip().lower())
            d['date'] = comment.published.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(d)
            comments.append(d)
        r = jsonify({'data': comments})
        r.status_code = 200
    except:
        logger.warn('bad request')
        r = jsonify({'data': []})
        r.status_code = 400
    return r


@app.route("/comments/count", methods=['GET'])
def get_comments_count():
    try:
        token = request.args.get('token', '')
        url = request.args.get('url', '')
        count = Comment.select(Comment).join(Site).where(
            (Comment.url == url) &
            (Comment.published.is_null(False)) &
            (Site.token == token)).count()
        r = jsonify({'count': count})
        r.status_code = 200
    except:
        r = jsonify({'count': 0})
        r.status_code = 200
    return r


@app.route("/comments", methods=['POST'])
def new_comment():

    try:
        data = request.get_json()
        logger.info(data)

        # validate token: retrieve site entity
        token = data.get('token', '')
        site = Site.select().where(Site.token == token).get()
        if site is None:
            logger.warn('Unknown site %s' % token)
            abort(400)

        # honeypot for spammers
        captcha = data.get('captcha', '')
        if captcha:
            logger.warn('discard spam: data %s' % data)
            abort(400)

        processor.enqueue({'request': 'new_comment', 'data': data})

    except:
        logger.exception("new comment failure")
        abort(400)

    return "OK"


@app.route("/report", methods=['GET'])
def report():

    try:
        token = request.args.get('token', '')
        secret = request.args.get('secret', '')

        if secret != config.SECRET:
            logger.warn('Unauthorized request')
            abort(401)

        site = Site.select().where(Site.token == token).get()
        if site is None:
            logger.warn('Unknown site %s' % token)
            abort(404)

        processor.enqueue({'request': 'report', 'data': token})


    except:
        logger.exception("report failure")
        abort(500)

    return "OK"


@app.route("/accept", methods=['GET'])
def accept_comment():

    try:
        id = request.args.get('comment', 0)
        secret = request.args.get('secret', '')

        if secret != config.SECRET:
            logger.warn('Unauthorized request')
            abort(401)

        processor.enqueue({'request': 'late_accept', 'data': id})

    except:
        logger.exception("accept failure")
        abort(500)

    return "PUBLISHED"


@app.route("/reject", methods=['GET'])
def reject_comment():

    try:
        id = request.args.get('comment', 0)
        secret = request.args.get('secret', '')

        if secret != config.SECRET:
            logger.warn('Unauthorized request')
            abort(401)

        processor.enqueue({'request': 'late_reject', 'data': id})

    except:
        logger.exception("reject failure")
        abort(500)

    return "REJECTED"

