#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from enum import Enum


class ConfigParameter(Enum):
    DB = "main.db"
    LANG = "main.lang"

    HTTP_HOST = "http.host"
    HTTP_PORT = "http.port"

    RSS_FILE = "rss.file"

    SMTP_HOST = "smtp.host"
    SMTP_PORT = "smtp.port"
    SMTP_LOGIN = "smtp.login"
    SMTP_PASSWORD = "smtp.password"

    SITE_PROTO = "site.proto"
    SITE_NAME = "site.name"
    SITE_URL = "site.url"
    SITE_ADMIN_EMAIL = "site.admin_email"
    SITE_REDIRECT = "site.redirect"

    WEB_USERNAME = "web.username"
    WEB_PASSWORD = "web.password"


class Config:

    _cfg = configparser.ConfigParser()

    def load(self, config_pathname):
        self._cfg.read(config_pathname)

    @staticmethod
    def _split_key(key: ConfigParameter):
        section, param = str(key.value).split(".")
        if not param:
            param = section
            section = ""
        return section, param

    def exists(self, key: ConfigParameter):
        section, param = self._split_key(key)
        return self._cfg.has_option(section, param)

    def get(self, key: ConfigParameter) -> str:
        section, param = self._split_key(key)
        return (
            self._cfg.get(section, param)
            if self._cfg.has_option(section, param)
            else ""
        )

    def put(self, key: ConfigParameter, value):
        section, param = self._split_key(key)
        if section and not self._cfg.has_section(section):
            self._cfg.add_section(section)
        self._cfg.set(section, param, str(value))

    def get_int(self, key: ConfigParameter) -> int:
        value = self.get(key)
        return int(value) if value else 0

    def get_bool(self, key: ConfigParameter) -> bool:
        value = self.get(key)
        assert value in (
            "yes",
            "true",
            "no",
            "false",
        ), f"Parameètre booléen incorrect {key.value}"
        return value in ("yes", "true")

    def check(self):
        for key in ConfigParameter:
            if not self.get(key):
                return False, key.value
        return True, None

    def __repr__(self):
        dict_repr = {}
        for section in self._cfg.sections():
            for option in self._cfg.options(section):
                dict_repr[".".join([section, option])] = self._cfg.get(section, option)
        return str(dict_repr)
