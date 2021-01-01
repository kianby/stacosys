#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest
import stacosys.conf.config as config

EXPECTED_DB_URL = "sqlite:///db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_IMAP_PORT = "5000"
EXPECTED_IMAP_LOGIN = "user"


@pytest.fixture
def conf():
    conf = config.Config()
    conf.put(config.DB_URL, EXPECTED_DB_URL)
    conf.put(config.HTTP_PORT, EXPECTED_HTTP_PORT)
    conf.put(config.IMAP_PORT, EXPECTED_IMAP_PORT)
    conf.put(config.SMTP_STARTTLS, "yes")
    conf.put(config.IMAP_SSL, "false")
    return conf


def test_exists(conf):
    assert conf is not None
    assert conf.exists(config.DB_URL)
    assert not conf.exists(config.IMAP_HOST)


def test_get(conf):
    assert conf is not None
    assert conf.get(config.DB_URL) == EXPECTED_DB_URL
    assert conf.get(config.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(config.HTTP_HOST) is None
    assert conf.get(config.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(config.IMAP_PORT) == EXPECTED_IMAP_PORT
    assert conf.get_int(config.IMAP_PORT) == int(EXPECTED_IMAP_PORT)
    try:
        conf.get_int(config.HTTP_PORT)
        assert False
    except:
        pass
    assert conf.get_bool(config.SMTP_STARTTLS)
    assert not conf.get_bool(config.IMAP_SSL)
    try:
        conf.get_bool(config.DB_URL)
        assert False
    except:
        pass


def test_put(conf):
    assert conf is not None
    assert not conf.exists(config.IMAP_LOGIN)
    conf.put(config.IMAP_LOGIN, EXPECTED_IMAP_LOGIN)
    assert conf.exists(config.IMAP_LOGIN)
    assert conf.get(config.IMAP_LOGIN) == EXPECTED_IMAP_LOGIN
