#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import ForeignKeyField
from core.database import get_db
from models.site import Site


class Reader(Model):
    url = CharField()
    email = CharField(default='')
    site = ForeignKeyField(Site, related_name='reader_site')

    class Meta:
        database = get_db()
