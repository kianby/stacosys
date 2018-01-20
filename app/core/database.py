#!/usr/bin/python
# -*- coding: UTF-8 -*-

from conf import config
import functools
from playhouse.db_url import connect


def get_db():
    return connect(config.general['db_url'])


def provide_db(func):

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        return func(get_db(), *args, **kwargs)

    return new_function


@provide_db
def setup(db):
    from models.site import Site
    from models.comment import Comment
    from models.reader import Reader
    from models.report import Report

    db.create_tables([Site, Comment, Reader, Report], safe=True)
