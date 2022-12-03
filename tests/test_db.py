#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

import pytest

from stacosys.db import dao, database
from stacosys.model.comment import Comment


@pytest.fixture
def setup_db():
    database.configure("sqlite:memory://db.sqlite")


def equals_comment(comment: Comment, other):
    return (
        comment.id == other.id
        and comment.author_gravatar == other.author_gravatar
        and comment.author_name == other.author_name
        and comment.author_site == other.author_site
        and comment.content == other.content
        and comment.created == other.created
        and comment.notified == other.notified
        and comment.published == other.published
    )


def test_find_comment_by_id(setup_db):
    assert dao.find_comment_by_id(1) is None
    c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
    assert c1.id is not None
    find_c1 = dao.find_comment_by_id(c1.id)
    assert find_c1
    assert equals_comment(c1, find_c1)
    c1.id = find_c1.id
    dao.delete_comment(c1)
    assert dao.find_comment_by_id(c1.id) is None


def test_dao_published(setup_db):
    assert 0 == dao.count_published_comments("")
    c1 = dao.create_comment("/post1", "Yax", "", "", "Comment 1")
    assert 0 == dao.count_published_comments("")
    assert 1 == len(dao.find_not_published_comments())
    dao.publish_comment(c1)
    assert 1 == dao.count_published_comments("")
    c2 = dao.create_comment("/post2", "Yax", "", "", "Comment 2")
    dao.publish_comment(c2)
    assert 2 == dao.count_published_comments("")
    c3 = dao.create_comment("/post2", "Yax", "", "", "Comment 3")
    dao.publish_comment(c3)
    assert 0 == len(dao.find_not_published_comments())

    # count published
    assert 1 == dao.count_published_comments("/post1")
    assert 2 == dao.count_published_comments("/post2")

    # find published
    assert 0 == len(dao.find_published_comments_by_url("/"))
    assert 1 == len(dao.find_published_comments_by_url("/post1"))
    assert 2 == len(dao.find_published_comments_by_url("/post2"))


def test_dao_notified(setup_db):
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


def create_comment(url, author_name, content):
    return dao.create_comment(url, author_name, "", "", content)


def test_find_recent_published_comments(setup_db):

    comments = []
    comments.append(create_comment("/post", "Adam", "Comment 1"))
    comments.append(create_comment("/post", "Arf", "Comment 2"))
    comments.append(create_comment("/post", "Arwin", "Comment 3"))
    comments.append(create_comment("/post", "Bill", "Comment 4"))
    comments.append(create_comment("/post", "Bo", "Comment 5"))
    comments.append(create_comment("/post", "Charles", "Comment 6"))
    comments.append(create_comment("/post", "Dan", "Comment 7"))
    comments.append(create_comment("/post", "Dwayne", "Comment 8"))
    comments.append(create_comment("/post", "Erl", "Comment 9"))
    comments.append(create_comment("/post", "Jay", "Comment 10"))
    comments.append(create_comment("/post", "Kenny", "Comment 11"))
    comments.append(create_comment("/post", "Lord", "Comment 12"))

    rows = dao.find_recent_published_comments()
    assert len(rows) == 0

    # publish every second
    for comment in comments:
        dao.publish_comment(comment)
        time.sleep(1)

    rows = dao.find_recent_published_comments()
    assert len(rows) == 10

    authors = [row.author_name for row in rows]
    assert authors == [
        "Lord",
        "Kenny",
        "Jay",
        "Erl",
        "Dwayne",
        "Dan",
        "Charles",
        "Bo",
        "Bill",
        "Arwin",
    ]
