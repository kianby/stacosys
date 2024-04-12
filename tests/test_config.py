#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pytest

from stacosys.service.configuration import Config, ConfigParameter

EXPECTED_DB = "sqlite://db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_LANG = "fr"

config = Config()


@pytest.fixture
def init_config():
    config.put(ConfigParameter.DB, EXPECTED_DB)
    config.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)


def test_split_key():
    section, param = config._split_key(ConfigParameter.HTTP_PORT)
    assert section == "http" and param == "port"


def test_exists(init_config):
    assert config.exists(ConfigParameter.DB)


def test_get(init_config):
    assert config.get(ConfigParameter.DB) == EXPECTED_DB
    assert config.get(ConfigParameter.HTTP_HOST) == ""
    assert config.get(ConfigParameter.HTTP_PORT) == str(EXPECTED_HTTP_PORT)
    assert config.get_int(ConfigParameter.HTTP_PORT) == EXPECTED_HTTP_PORT
    with pytest.raises(AssertionError):
        config.get_bool(ConfigParameter.DB)


def test_put(init_config):
    assert not config.exists(ConfigParameter.LANG)
    config.put(ConfigParameter.LANG, EXPECTED_LANG)
    assert config.exists(ConfigParameter.LANG)
    assert config.get(ConfigParameter.LANG) == EXPECTED_LANG


def test_check(init_config):
    success, error = config.check()
    assert not success and error
