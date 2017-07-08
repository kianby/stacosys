#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from sanic import response
from app import app
from app.services import processor

logger = logging.getLogger(__name__)


@app.route("/unsubscribe", methods=['GET'])
def unsubscribe(request):

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
        return response.text('BAD_REQUEST', status=400)

    return response.text('OK')
