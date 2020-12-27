#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from peewee import TextField
from peewee import DateTimeField
from peewee import ForeignKeyField
from stacosys.model.site import Site
from stacosys.core.database import get_db
from datetime import datetime


class Comment(Model):
    url = CharField()
    created = DateTimeField()
    notified = DateTimeField(null=True, default=None)
    published = DateTimeField(null=True, default=None)
    author_name = CharField()
    author_site = CharField(default='')
    author_gravatar = CharField(default='')
    content = TextField()
    site = ForeignKeyField(Site, related_name='site')

    class Meta:
        database = get_db()

    def notify_site_admin(self):
        self.notified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save()

    def publish(self):
        self.published = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save()
