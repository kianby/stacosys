#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import CharField, DateTimeField, TextField

from stacosys.db.database import BaseModel


class Comment(BaseModel):
    url = CharField()
    created = DateTimeField()
    notified = DateTimeField(null=True, default=None)
    published = DateTimeField(null=True, default=None)
    author_name = CharField()
    author_site = CharField(default="")
    author_gravatar = CharField(default="")
    content = TextField()
