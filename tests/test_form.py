#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging

import pytest

from stacosys.db import database
from stacosys.interface import app
from stacosys.interface import form


@pytest.fixture
def client():
    logger = logging.getLogger(__name__)
    database.setup(":memory:")
    app.config.update(SITE_REDIRECT="/redirect")
    logger.info(f"start interface {form}")
    return app.test_client()


def test_new_comment_honeypot(client):
    resp = client.post(
        "/newcomment", content_type="multipart/form-data", data={"remarque": "trapped"}
    )
    assert resp.status == "400 BAD REQUEST"


def test_new_comment_success(client):
    resp = client.post(
        "/newcomment",
        content_type="multipart/form-data",
        data={"author": "Jack", "url": "/site3", "message": "comment 3"},
    )
    assert resp.status == "302 FOUND"


def test_check_form_data():
    from stacosys.interface.form import check_form_data

    assert check_form_data({"author": "Jack", "url": "/site3", "message": "comment 3"})
    assert not check_form_data(
        {"author": "Jack", "url": "/site3", "message": "comment 3", "extra": "ball"}
    )
