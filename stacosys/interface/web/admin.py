#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import logging

from flask import request, redirect, flash, render_template, session

from stacosys.db import dao
from stacosys.interface import app

logger = logging.getLogger(__name__)


def is_login_ok(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest().upper()
    return app.config.get("WEB_USERNAME") == username and app.config.get("WEB_PASSWORD") == hashed


@app.route('/web/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if is_login_ok(username, password):
            session['user'] = username
            return redirect('/web/admin')

        flash("Identifiant ou mot de passe incorrect")
        return redirect('/web/login')

    return render_template("login_" + app.config.get("LANG") + ".html")


@app.route('/web/logout', methods=["GET"])
def logout():
    session.pop('user')
    return redirect('/web/login')


@app.route("/web/admin", methods=["GET"])
def admin_homepage():
    if not ('user' in session and session['user'] == app.config.get("WEB_USERNAME")):
        flash("Vous avez été déconnecté.")
        return redirect('/web/login')

    comments = dao.find_not_published_comments()
    return render_template("admin_" + app.config.get("LANG") + ".html", comments=comments,
                           baseurl=app.config.get("SITE_URL"))


@app.route("/web/admin", methods=["POST"])
def admin_action():
    flash(request.form.get("comment") + " " + request.form.get("action"))
    return redirect('/web/admin')
