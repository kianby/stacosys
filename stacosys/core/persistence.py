#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from stacosys.conf import config


class Persistence:
    def __init__(self):
        db_file = config.get(config.DB_FILE)
        if db_file:
            self.db = TinyDB(db_file, sort_keys=True, indent=4, separators=(",", ": "))
        else:
            self.db = TinyDB(storage=MemoryStorage)

    def get_db(self):
        return self.db

    def get_table_comments(self):
        return self.db.table("comments")
