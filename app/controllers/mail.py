#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from flask import request, abort
from app import app
from app.services import processor

logger = logging.getLogger(__name__)


@app.route("/inbox", methods=['POST'])
def new_mail():

    try:
        data = request.get_json()
        logger.debug(data)

        processor.enqueue({'request': 'new_mail', 'data': data})

    except:
        logger.exception("new mail failure")
        abort(400)

    return "OK"
