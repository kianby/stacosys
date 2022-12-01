#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydal import DAL, Field


class Database:

    db_dal = DAL()

    def configure(self, db_uri):
        self.db_dal = DAL(db_uri, migrate=db_uri.startswith("sqlite:memory"))
        self.db_dal.define_table(
            "comment",
            Field("url"),
            Field("created", type="datetime"),
            Field("notified", type="datetime"),
            Field("published", type="datetime"),
            Field("author_name"),
            Field("author_site"),
            Field("author_gravatar"),
            Field("content", type="text"),
        )

    def get(self):
        return self.db_dal


database = Database()
db = database.get
