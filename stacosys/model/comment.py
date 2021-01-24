#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import CharField
from peewee import TextField
from peewee import DateTimeField
from datetime import datetime
from stacosys.core.database import BaseModel


class Comment(BaseModel):
    url = CharField()
    created = DateTimeField()
    notified = DateTimeField(null=True, default=None)
    published = DateTimeField(null=True, default=None)
    author_name = CharField()
    author_site = CharField(default="")
    author_gravatar = CharField(default="")
    content = TextField()

    def notify_site_admin(self):
        self.notified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def publish(self):
        self.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()
