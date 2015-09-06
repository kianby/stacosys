#!/usr/bin/python
# -*- coding: UTF-8 -*-

import config
import functools
from playhouse.db_url import connect


def get_db():
    return connect(config.DB_URL)


def provide_db(func):

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        return func(get_db(), *args, **kwargs)

    return new_function


@provide_db
def setup(db):
    from app.models.site import Site
    from app.models.comment import Comment
    from app.models.reader import Reader
    from app.models.report import Report

    db.create_tables([Site, Comment, Reader, Report], safe=True)
