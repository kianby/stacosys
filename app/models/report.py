#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import BooleanField
from peewee import ForeignKeyField
from app.services.database import get_db
from app.models.site import Site

class Report(Model):
    name = CharField(unique=True)
    email = CharField()
    url = CharField()
    published = BooleanField(default=False)
    rejected = BooleanField(default=False)
    subscribed = BooleanField(default=False)
    unsubscribed = BooleanField(default=False)
    site = ForeignKeyField(Site, related_name='report_site')

    class Meta:
        database = get_db()
