#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, jsonify, abort, redirect
from core import app
from models.site import Site
from models.comment import Comment
from helpers.hashing import md5
from core import processor

logger = logging.getLogger(__name__)

@app.route("/newcomment", methods=['POST'])
def new_form_comment():

    try:
        data = request.form
        logger.info('headers: {}'.format(request.headers))
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

    return redirect('/redirect/', code=302)