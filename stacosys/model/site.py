#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from stacosys.core.database import get_db


class Site(Model):
    name = CharField(unique=True)
    url = CharField()
    token = CharField()
    admin_email = CharField()

    class Meta:
        database = get_db()
