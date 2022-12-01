#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pytest

from stacosys.db import dao
from stacosys.db import database

@pytest.fixture
def setup_db():
    database.configure("sqlite:memory://db.sqlite")


def test_dao_published(setup_db):

    # test count published
    assert 0 == dao.count_published_comments("")
    c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
    assert 0 == dao.count_published_comments("")
    dao.publish_comment(c1)
    assert 1 == dao.count_published_comments("")
    c2 = dao.create_comment("/post2", "Yax", "", "", "Comment 2")
    dao.publish_comment(c2)
    assert 2 == dao.count_published_comments("")
    c3 = dao.create_comment("/post2", "Yax", "", "", "Comment 3")
    dao.publish_comment(c3)
    assert 1 == dao.count_published_comments("/post1")
    assert 2 == dao.count_published_comments("/post2")

    # test find published
    assert 0 == len(dao.find_published_comments_by_url("/"))
    assert 1 == len(dao.find_published_comments_by_url("/post1"))
    assert 2 == len(dao.find_published_comments_by_url("/post2"))

    dao.delete_comment(c1)
    assert 0 == len(dao.find_published_comments_by_url("/post1"))

def test_dao_notified(setup_db):

    # test count notified
    assert 0 == len(dao.find_not_notified_comments())
    c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
    assert 1 == len(dao.find_not_notified_comments())
    c2 = dao.create_comment("/post2", "Yax", "", "", "Comment 2")
    assert 2 == len(dao.find_not_notified_comments())
    dao.notify_comment(c1)
    dao.notify_comment(c2)
    assert 0 == len(dao.find_not_notified_comments())
    c3 = dao.create_comment("/post2", "Yax", "", "", "Comment 3")
    assert 1 == len(dao.find_not_notified_comments())
    dao.notify_comment(c3)
    assert 0 == len(dao.find_not_notified_comments())

