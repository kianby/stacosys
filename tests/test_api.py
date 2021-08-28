#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

import pytest

from stacosys.db import database
from stacosys.interface import api
from stacosys.interface import app


@pytest.fixture
def client():
    logger = logging.getLogger(__name__)
    db = database.Database()
    db.setup(":memory:")
    app.config.update(SITE_TOKEN="ETC")
    logger.info(f"start interface {api}")
    return app.test_client()


def test_api_ping(client):
    rv = client.get('/ping')
    assert rv.data == b"OK"


def test_api_count(client):
    rv = client.get('/comments/count')
    assert b'{"count":0}\n' in rv.data
