#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

import configparser


class ConfigParameter(Enum):
    DB_SQLITE_FILE = "main.db_sqlite_file"
    LANG = "main.lang"

    HTTP_HOST = "http.host"
    HTTP_PORT = "http.port"

    RSS_PROTO = "rss.proto"
    RSS_FILE = "rss.file"

    SMTP_HOST = "smtp.host"
    SMTP_PORT = "smtp.port"
    SMTP_LOGIN = "smtp.login"
    SMTP_PASSWORD = "smtp.password"

    SITE_NAME = "site.name"
    SITE_URL = "site.url"
    SITE_ADMIN_EMAIL = "site.admin_email"
    SITE_REDIRECT = "site.redirect"

    WEB_USERNAME = "web.username"
    WEB_PASSWORD = "web.password"


class Config:
    def __init__(self):
        self._cfg = configparser.ConfigParser()

    @classmethod
    def load(cls, config_pathname):
        config = cls()
        config._cfg.read(config_pathname)
        return config

    def _split_key(self, key: ConfigParameter):
        section, param = str(key.value).split(".")
        if not param:
            param = section
            section = None
        return (section, param)

    def exists(self, key: ConfigParameter):
        section, param = self._split_key(key)
        return self._cfg.has_option(section, param)

    def get(self, key: ConfigParameter):
        section, param = self._split_key(key)
        return (
            self._cfg.get(section, param)
            if self._cfg.has_option(section, param)
            else None
        )

    def put(self, key: ConfigParameter, value):
        section, param = self._split_key(key)
        if section and not self._cfg.has_section(section):
            self._cfg.add_section(section)
        self._cfg.set(section, param, str(value))

    def get_int(self, key: ConfigParameter):
        value = self.get(key)
        return int(value) if value else 0

    def get_bool(self, key: ConfigParameter):
        value = self.get(key)
        assert value in ("yes", "true", "no", "false")
        return value in ("yes", "true")

    def check(self):
        for key in ConfigParameter:
            assert self.get(key), f"Paramètre introuvable : {key.value}"

    def __repr__(self):
        d = dict()
        for section in self._cfg.sections():
            for option in self._cfg.options(section):
                d[".".join([section, option])] = self._cfg.get(section, option)
        return str(d)
