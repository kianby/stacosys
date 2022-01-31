#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

import profig


class ConfigParameter(Enum):
    DB_SQLITE_FILE = "main.db_sqlite_file"
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
    SMTP_SSL = "smtp.ssl"
    SMTP_HOST = "smtp.host"
    SMTP_PORT = "smtp.port"
    SMTP_LOGIN = "smtp.login"
    SMTP_PASSWORD = "smtp.password"

    SITE_NAME = "site.name"
    SITE_URL = "site.url"
    SITE_TOKEN = "site.token"
    SITE_ADMIN_EMAIL = "site.admin_email"
    SITE_REDIRECT = "site.redirect"

    WEB_USERNAME = "web.username"
    WEB_PASSWORD = "web.password"


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

    def exists(self, key: ConfigParameter):
        return key.value in self._params

    def get(self, key: ConfigParameter):
        return self._params[key.value] if key.value in self._params else None

    def put(self, key: ConfigParameter, value):
        self._params[key.value] = value

    def get_int(self, key: ConfigParameter):
        return int(self._params[key.value])

    def get_bool(self, key: ConfigParameter):
        value = self._params[key.value].lower()
        assert value in ("yes", "true", "no", "false")
        return value in ("yes", "true")

    def __repr__(self):
        return self._params.__repr__()
