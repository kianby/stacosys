#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime

from stacosys.model.comment import Comment


def find_comment_by_id(id):
    return Comment.get_by_id(id)


def notify_comment(comment: Comment):
    comment.notified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()


def publish_comment(comment: Comment):
    comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()


def delete_comment(comment: Comment):
    comment.delete_instance()


def find_not_notified_comments():
    return Comment.select().where(Comment.notified.is_null())


def find_published_comments_by_url(url):
    return Comment.select(Comment).where((Comment.url == url) & (Comment.published.is_null(False))).order_by(
        +Comment.published)


def count_published_comments(url):
    return Comment.select(Comment).where(
        (Comment.url == url) & (Comment.published.is_null(False))).count() if url else Comment.select(Comment).where(
        Comment.published.is_null(False)).count()


def create_comment(url, author_name, author_site, author_gravatar, message):
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment = Comment(
        url=url,
        author_name=author_name,
        author_site=author_site,
        author_gravatar=author_gravatar,
        content=message,
        created=created,
        notified=None,
        published=None,
    )
    comment.save()
    return comment
