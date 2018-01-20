#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from conf import config
from flask import request, jsonify, abort
from core import app
from models.site import Site
from models.comment import Comment
from helpers.hashing import md5
from core import processor

logger = logging.getLogger(__name__)

@app.route("/report", methods=['GET'])
def report():

    try:
        token = request.args.get('token', '')
        secret = request.args.get('secret', '')

        if secret != config.security['secret']:
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
        id = request.args.get('comment', '')
        secret = request.args.get('secret', '')

        if secret != config.security['secret']:
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
        id = request.args.get('comment', '')
        secret = request.args.get('secret', '')

        if secret != config.security['secret']:
            logger.warn('Unauthorized request')
            abort(401)

        processor.enqueue({'request': 'late_reject', 'data': id})

    except:
        logger.exception("reject failure")
        abort(500)

    return "REJECTED"
