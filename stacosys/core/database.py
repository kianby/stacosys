#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
from tinydb import TinyDB
from stacosys.conf import config


def get_db():
    return connect(config.get(config.DB_URL))


def setup():
    from stacosys.model.site import Site
    from stacosys.model.comment import Comment

    get_db().create_tables([Site, Comment], safe=True)
    if config.exists(config.DB_BACKUP_JSON_FILE):
        _backup_db(config.DB_BACKUP_JSON_FILE, Comment)


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
