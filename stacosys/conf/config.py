#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

# constants
FLASK_APP = "flask.app"

DB_URL = "main.db_url"
DB_BACKUP_JSON_FILE = "main.db_backup_json_file"
LANG = "main.lang"
COMMENT_POLLING = "main.newcomment_polling"

HTTP_HOST = "http.host"
HTTP_PORT = "http.port"

RSS_PROTO = "rss.proto"
RSS_FILE = "rss.file"

IMAP_POLLING = "imap.polling"
IMAP_SSL = "imap.ssl"
IMAP_HOST = "imap.host"
IMAP_PORT = "imap.port"
IMAP_LOGIN = "imap.login"
IMAP_PASSWORD = "imap.password"

SMTP_STARTTLS = "smtp.starttls"
SMTP_HOST = "smtp.host"
SMTP_PORT = "smtp.port"
SMTP_LOGIN = "smtp.login"
SMTP_PASSWORD = "smtp.password"

SITE_NAME = "site.name"
SITE_URL = "site.url"
SITE_TOKEN = "site.token"
SITE_ADMIN_EMAIL = "site.admin_email"


class Config:
    def __init__(self):
        self._params = dict()

    @classmethod
    def load(cls, config_pathname):
        cfg = profig.Config(config_pathname)
        cfg.sync()
        config = cls()
        config._params.update(cfg)
        return config

    def exists(self, key):
        return key in self._params

    def get(self, key):
        return self._params[key] if key in self._params else None

    def put(self, key, value):
        self._params[key] = value

    def get_int(self, key):
        return int(self._params[key])

    def get_bool(self, key):
        return self._params[key].lower() in ("yes", "true")

