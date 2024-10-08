#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging

import pytest

from stacosys.db import database
from stacosys.interface import app, form
from stacosys.service.configuration import Config
from stacosys.service.mail import Mailer
from stacosys.service.rssfeed import Rss


@pytest.fixture
def client():
    logger = logging.getLogger(__name__)
    database.configure("sqlite:memory://db.sqlite")
    logger.info(f"start interface {form}")
    app.config["CONFIG"] = Config()
    app.config["MAILER"] = Mailer()
    app.config["RSS"] = Rss()
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
