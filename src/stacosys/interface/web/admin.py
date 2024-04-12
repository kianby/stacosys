#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import logging

from flask import flash, redirect, render_template, request, session

from stacosys.db import dao
from stacosys.interface import app
from stacosys.service.configuration import ConfigParameter

logger = logging.getLogger(__name__)

app.add_url_rule("/web", endpoint="index")
app.add_url_rule("/web/", endpoint="index")


@app.endpoint("index")
def index():
    return redirect("/web/admin")


def is_login_ok(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest().upper()
    return (
        app.config['CONFIG'].get(ConfigParameter.WEB_USERNAME) == username
        and app.config['CONFIG'].get(ConfigParameter.WEB_PASSWORD) == hashed
    )


@app.route("/web/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if is_login_ok(username, password):
            session["user"] = username
            return redirect("/web/admin")
        # TODO localization
        flash("Identifiant ou mot de passe incorrect")
        return redirect("/web/login")
    # GET
    return render_template("login_" + app.config['CONFIG'].get(ConfigParameter.LANG) + ".html")


@app.route("/web/logout", methods=["GET"])
def logout():
    session.pop("user")
    return redirect("/web/admin")


@app.route("/web/admin", methods=["GET"])
def admin_homepage():
    if not (
        "user" in session
        and session["user"] == app.config['CONFIG'].get(ConfigParameter.WEB_USERNAME)
    ):
        # TODO localization
        flash("Vous avez été déconnecté.")
        return redirect("/web/login")

    comments = dao.find_not_published_comments()
    return render_template(
        "admin_" + app.config['CONFIG'].get(ConfigParameter.LANG) + ".html",
        comments=comments,
        baseurl=app.config['CONFIG'].get(ConfigParameter.SITE_URL),
    )


@app.route("/web/admin", methods=["POST"])
def admin_action():
    comment = dao.find_comment_by_id(request.form.get("comment"))
    if comment is None:
        # TODO localization
        flash("Commentaire introuvable")
    elif request.form.get("action") == "APPROVE":
        dao.publish_comment(comment)
        app.config['RSS'].generate()
        # TODO localization
        flash("Commentaire publié")
    else:
        dao.delete_comment(comment)
        # TODO localization
        flash("Commentaire supprimé")
    return redirect("/web/admin")
