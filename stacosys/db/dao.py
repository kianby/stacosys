#!/usr/bin/python
# -*- coding: UTF-8 -*-
# pylint: disable=singleton-comparison

from datetime import datetime

from stacosys.db import db
from stacosys.model.comment import Comment


def find_comment_by_id(comment_id):
    return db().comment(comment_id)


def notify_comment(comment: Comment):
    db()(db().comment.id == comment.id).update(notified=datetime.now())
    db().commit()


def publish_comment(comment: Comment):
    db()(db().comment.id == comment.id).update(published=datetime.now())
    db().commit()


def delete_comment(comment: Comment):
    db()(db().comment.id == comment.id).delete()
    db().commit()


def find_not_notified_comments():
    return db()(db().comment.notified is None).select()


def find_not_published_comments():
    return db()(db().comment.published is None).select()


def find_published_comments_by_url(url):
    return db()((db().comment.url == url) & (db().comment.published is not None)).select(
        orderby=db().comment.published
    )


def count_published_comments(url):
    return (
        db()((db().comment.url == url) & (db().comment.published is not None)).count()
        if url
        else db()(db().comment.published is not None).count()
    )


def find_recent_published_comments():
    return db()(db().comment.published is not None).select(
        orderby=~db().comment.published, limitby=(0, 10)
    )


def create_comment(url, author_name, author_site, author_gravatar, message):
    row = db().comment.insert(
        url=url,
        author_name=author_name,
        author_site=author_site,
        author_gravatar=author_gravatar,
        content=message,
        created=datetime.now(),
        notified=None,
        published=None,
    )
    db().commit()
    return Comment(
        id=row.id,
        url=row.url,
        author_name=row.author_name,
        author_site=row.author_site,
        author_gravatar=row.author_gravatar,
        content=row.content,
        created=row.created,
        notified=row.notified,
        published=row.published,
    )
