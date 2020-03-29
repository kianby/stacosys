#!/usr/bin/python
# -*- coding: UTF-8 -*-

from playhouse.db_url import connect

from conf import config


def get_db():
    return connect(config.get(config.DB_URL))


def setup():
    from model.site import Site
    from model.comment import Comment

    get_db().create_tables([Site, Comment], safe=True)
