#!/usr/bin/python
# -*- coding: UTF-8 -*-

from playhouse.db_url import connect

from stacosys.conf import config


def get_db():
    return connect(config.get(config.DB_URL))


def setup():
    from stacosys.model.site import Site
    from stacosys.model.comment import Comment

    get_db().create_tables([Site, Comment], safe=True)

from playhouse.shortcuts import model_to_dict
import json

def tojson_model(comment):
    dcomment = model_to_dict(comment)
    del dcomment['site']
    tcomment = json.dumps(dcomment, indent=4, sort_keys=True, default=str)
    return json.loads(tcomment) 

def tojson_models(models):
    print(json.dumps(list(models.dicts()), indent=4, sort_keys=True, default=str))

def dump_db():
    from tinydb import TinyDB, Query
    from stacosys.model.comment import Comment
    db = TinyDB('db.json')
    for comment in Comment.select():
        cc = tojson_model(comment)
        print(cc)
        db.insert(cc)
