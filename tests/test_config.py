#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest
from stacosys.conf.config import Config, ConfigParameter

EXPECTED_DB_SQLITE_FILE = "db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_IMAP_PORT = "5000"
EXPECTED_IMAP_LOGIN = "user"


@pytest.fixture
def conf():
    conf = Config()
    conf.put(ConfigParameter.DB_SQLITE_FILE, EXPECTED_DB_SQLITE_FILE)
    conf.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)
    conf.put(ConfigParameter.IMAP_PORT, EXPECTED_IMAP_PORT)
    conf.put(ConfigParameter.SMTP_STARTTLS, "yes")
    conf.put(ConfigParameter.IMAP_SSL, "false")
    return conf


def test_exists(conf):
    assert conf is not None
    assert conf.exists(ConfigParameter.DB_SQLITE_FILE)
    assert not conf.exists(ConfigParameter.IMAP_HOST)


def test_get(conf):
    assert conf is not None
    assert conf.get(ConfigParameter.DB_SQLITE_FILE) == EXPECTED_DB_SQLITE_FILE
    assert conf.get(ConfigParameter.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(ConfigParameter.HTTP_HOST) is None
    assert conf.get(ConfigParameter.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(ConfigParameter.IMAP_PORT) == EXPECTED_IMAP_PORT
    assert conf.get_int(ConfigParameter.IMAP_PORT) == int(EXPECTED_IMAP_PORT)
    try:
        conf.get_int(ConfigParameter.HTTP_PORT)
        assert False
    except Exception:
        pass
    assert conf.get_bool(ConfigParameter.SMTP_STARTTLS)
    assert not conf.get_bool(ConfigParameter.IMAP_SSL)
    try:
        conf.get_bool(ConfigParameter.DB_URL)
        assert False
    except Exception:
        pass


def test_put(conf):
    assert conf is not None
    assert not conf.exists(ConfigParameter.IMAP_LOGIN)
    conf.put(ConfigParameter.IMAP_LOGIN, EXPECTED_IMAP_LOGIN)
    assert conf.exists(ConfigParameter.IMAP_LOGIN)
    assert conf.get(ConfigParameter.IMAP_LOGIN) == EXPECTED_IMAP_LOGIN
