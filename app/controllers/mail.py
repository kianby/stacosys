#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from sanic import response
from app import app
from app.services import processor

logger = logging.getLogger(__name__)


@app.route("/inbox", methods=['POST'])
def new_mail(request):

    try:
        data = request.json
        logger.debug(data)

        processor.enqueue({'request': 'new_mail', 'data': data})

    except:
        logger.exception("new mail failure")
        return response.text('BAD_REQUEST', status=400)

    return response.text('OK')
