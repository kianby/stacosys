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
        id = request.args.get('comment', '')
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
        id = request.args.get('comment', '')
        secret = request.args.get('secret', '')

        if secret != config.SECRET:
            logger.warn('Unauthorized request')
            abort(401)

        processor.enqueue({'request': 'late_reject', 'data': id})

    except:
        logger.exception("reject failure")
        abort(500)

    return "REJECTED"
