#!/usr/bin/python
# -*- coding: UTF-8 -*-

from peewee import Model
from peewee import CharField
from stacosys.core.database import BaseModel


class Site(BaseModel):
    name = CharField(unique=True)
    url = CharField()
    token = CharField()
    admin_email = CharField()
