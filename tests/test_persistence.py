#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest


@pytest.fixture
def persistence():
    from stacosys.conf import config

    config.params = {"main.db_file": None}
    from stacosys.core import persistence

    return persistence.Persistence()


def test_init_persistence(persistence):
    assert persistence is not None
    assert persistence.get_db() is not None
    assert persistence.get_table_comments() is not None
