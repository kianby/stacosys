#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField
from models.site import Site
from core.database import get_db


class Comment(Model):
    url = CharField()
    created = DateTimeField()
    notified = DateTimeField(null=True,default=None)
    published = DateTimeField(null=True, default=None)
    author_name = CharField()
    author_site = CharField(default='')
    author_gravatar = CharField(default='')
    ip = CharField(default='')
    content = TextField()
    site = ForeignKeyField(Site, related_name='site')

    class Meta:
        database = get_db()
