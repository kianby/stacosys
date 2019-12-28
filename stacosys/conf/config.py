#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

# constants
FLASK_APP = "flask.app"

DB_URL = "main.db_url"
LANG = "main.lang"

HTTP_HOST = "http.host"
HTTP_PORT = "http.port"

SECURITY_SALT = "security.salt"
SECURITY_SECRET = "security.secret"

RSS_PROTO = "rss.proto"
RSS_FILE = "rss.file"

MAIL_POLLING = "mail.fetch_polling"
COMMENT_POLLING = "main.newcomment_polling"
MAILER_URL = "mail.mailer_url"


# variable
params = dict()


def initialize(config_pathname, flask_app):
    cfg = profig.Config(config_pathname)
    cfg.sync()
    params.update(cfg)
    params.update({FLASK_APP: flask_app})


def get(key):
    return params[key]


def getInt(key):
    return int(params[key])


def _str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def getBool(key):
    return _str2bool(params[key])


def flaskapp():
    return params[FLASK_APP]
