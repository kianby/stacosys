#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest
from stacosys.conf.config import Config, Parameter

EXPECTED_DB_URL = "sqlite:///db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_IMAP_PORT = "5000"
EXPECTED_IMAP_LOGIN = "user"


@pytest.fixture
def conf():
    conf = Config()
    conf.put(Parameter.DB_URL, EXPECTED_DB_URL)
    conf.put(Parameter.HTTP_PORT, EXPECTED_HTTP_PORT)
    conf.put(Parameter.IMAP_PORT, EXPECTED_IMAP_PORT)
    conf.put(Parameter.SMTP_STARTTLS, "yes")
    conf.put(Parameter.IMAP_SSL, "false")
    return conf


def test_exists(conf):
    assert conf is not None
    assert conf.exists(Parameter.DB_URL)
    assert not conf.exists(Parameter.IMAP_HOST)


def test_get(conf):
    assert conf is not None
    assert conf.get(Parameter.DB_URL) == EXPECTED_DB_URL
    assert conf.get(Parameter.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(Parameter.HTTP_HOST) is None
    assert conf.get(Parameter.HTTP_PORT) == EXPECTED_HTTP_PORT
    assert conf.get(Parameter.IMAP_PORT) == EXPECTED_IMAP_PORT
    assert conf.get_int(Parameter.IMAP_PORT) == int(EXPECTED_IMAP_PORT)
    try:
        conf.get_int(Parameter.HTTP_PORT)
        assert False
    except:
        pass
    assert conf.get_bool(Parameter.SMTP_STARTTLS)
    assert not conf.get_bool(Parameter.IMAP_SSL)
    try:
        conf.get_bool(Parameter.DB_URL)
        assert False
    except:
        pass


def test_put(conf):
    assert conf is not None
    assert not conf.exists(Parameter.IMAP_LOGIN)
    conf.put(Parameter.IMAP_LOGIN, EXPECTED_IMAP_LOGIN)
    assert conf.exists(Parameter.IMAP_LOGIN)
    assert conf.get(Parameter.IMAP_LOGIN) == EXPECTED_IMAP_LOGIN
