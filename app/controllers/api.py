#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from app import app

logger = logging.getLogger(__name__)


@app.route("/comments", methods=['GET'])
def get_comments():
    return "OK"
