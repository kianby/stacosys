#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from playhouse.db_url import SqliteDatabase

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


def setup(db_url):
    db.init(db_url)
    db.connect()

    from stacosys.model.comment import Comment
    db.create_tables([Comment], safe=True)


def get_db():
    return db
