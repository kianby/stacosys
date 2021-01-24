#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from peewee import Model
from playhouse.db_url import SqliteDatabase
from playhouse.shortcuts import model_to_dict
from tinydb import TinyDB

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Database:
    def get_db(self):
        return db

    def setup(self, db_url):

        db.init(db_url)
        db.connect()

        from stacosys.model.comment import Comment
        db.create_tables([Comment], safe=True)


#        if config.exists(config.DB_BACKUP_JSON_FILE):
#            _backup_db(config.DB_BACKUP_JSON_FILE, Comment)


def _tojson_model(comment):
    dcomment = model_to_dict(comment)
    # del dcomment["site"]
    tcomment = json.dumps(dcomment, indent=4, sort_keys=True, default=str)
    return json.loads(tcomment)


def _backup_db(db_file, Comment):
    db = TinyDB(db_file, sort_keys=True, indent=4, separators=(",", ": "))
    db.drop_tables()
    table = db.table("comments")
    for comment in Comment.select():
        cc = _tojson_model(comment)
        table.insert(cc)
