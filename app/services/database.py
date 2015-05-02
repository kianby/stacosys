#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib
import config
import functools
from config import DB_URL
from playhouse.db_url import connect


def get_db():
    return connect(DB_URL)


def provide_db(func):

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        return func(get_db(), *args, **kwargs)

    return new_function


def hash(value):
    string = '%s%s' % (value, config.SALT)
    dk = hashlib.sha256(string.encode())
    return dk.hexdigest()


@provide_db
def setup(db):
    from app.models.site import Site
    from app.models.comment import Comment

    db.create_tables([Site, Comment], safe=True)
