#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, abort
from core import app
from core import processor

logger = logging.getLogger(__name__)


@app.route("/unsubscribe", methods=['GET'])
def unsubscribe():

    try:
        data = {
            'token': request.args.get('token', ''),
            'url': request.args.get('url', ''),
            'email': request.args.get('email', '')
        }
        logger.debug(data)

        processor.enqueue({'request': 'unsubscribe', 'data': data})

    except:
        logger.exception("unsubscribe failure")
        abort(400)

    return "OK"
