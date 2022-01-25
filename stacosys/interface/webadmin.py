#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from stacosys.core.templater import Templater, Template

from flask import jsonify, request
from flask import render_template

from stacosys.db import dao
from stacosys.interface import app

logger = logging.getLogger(__name__)


current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
templater = Templater(template_path)

@app.route("/web/comment", methods=["GET"])
def web_comment_approval():
    lang = "fr"
    return templater.get_template(lang, Template.WEB_COMMENT_APPROVAL).render(
        name="Yax")



