#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from flask import request, redirect, flash, render_template

from stacosys.db import dao
from stacosys.interface import app

logger = logging.getLogger(__name__)


@app.route("/web", methods=["GET"])
def admin_homepage():
    lang = "fr"
    comments = dao.find_not_published_comments()
    return render_template("admin_" + lang + ".html", comments=comments, baseurl=app.config.get("SITE_URL"))


@app.route("/web", methods=["POST"])
def admin_action():
    flash(request.form.get("comment") + " " + request.form.get("action"))
    return redirect('/web')
