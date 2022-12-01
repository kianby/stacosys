#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

from stacosys.service import config
from stacosys.service.configuration import ConfigParameter

EXPECTED_DB_SQLITE_FILE = "sqlite://db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_LANG = "fr"


@pytest.fixture
def init_config():
    config.put(ConfigParameter.DB, EXPECTED_DB_SQLITE_FILE)
    config.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)    

def test_exists(init_config):
    assert config.exists(ConfigParameter.DB)

def test_get(init_config):
    assert config.get(ConfigParameter.DB) == EXPECTED_DB_SQLITE_FILE
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
