#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import ForeignKeyField
from app.models.site import Site
from app.services.database import get_db


class Comment(Model):
    url = CharField()
    date = DateTimeField()
    rel_index = IntegerField()
    author_name = CharField()
    author_email = CharField(default='')
    author_site = CharField()
    content = CharField()
    site = ForeignKeyField(Site, related_name='site')

    class Meta:
        database = get_db()
