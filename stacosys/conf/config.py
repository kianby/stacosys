#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

# constants
FLASK_APP = 'flask.app'

DB_URL = 'main.db_url'
DB_FILE = 'main.db_file'
LANG = 'main.lang'
COMMENT_POLLING = 'main.newcomment_polling'

HTTP_HOST = 'http.host'
HTTP_PORT = 'http.port'

RSS_PROTO = 'rss.proto'
RSS_FILE = 'rss.file'

IMAP_POLLING = 'imap.polling'
IMAP_SSL = 'imap.ssl'
IMAP_HOST = 'imap.host'
IMAP_PORT = 'imap.port'
IMAP_LOGIN = 'imap.login'
IMAP_PASSWORD = 'imap.password'

SMTP_STARTTLS = 'smtp.starttls'
SMTP_HOST = 'smtp.host'
SMTP_PORT = 'smtp.port'
SMTP_LOGIN = 'smtp.login'
SMTP_PASSWORD = 'smtp.password'

SITE_NAME = 'site.name'
SITE_URL = 'site.url'
SITE_TOKEN = 'site.token'
SITE_ADMIN_EMAIL = 'site.admin_email'

# variable
params = dict()


def initialize(config_pathname, flask_app):
    cfg = profig.Config(config_pathname)
    cfg.sync()
    params.update(cfg)
    params.update({FLASK_APP: flask_app})


def get(key):
    return params[key]


def get_int(key):
    return int(params[key])


def get_bool(key):
    return params[key].lower() in ('yes', 'true', '1')


def flaskapp():
    return params[FLASK_APP]
