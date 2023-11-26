#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sqlite3

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

# What script performs:
# - first, remove site table: crash here if table doesn't exist
#          (compatibility test without effort)
# - remove site_id column from comment table
script = """
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
DROP TABLE site;
ALTER TABLE comment RENAME TO _comment_old;
CREATE TABLE comment (
    id INTEGER NOT NULL PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    notified DATETIME,
    created DATETIME NOT NULL,
    published DATETIME,
    author_name VARCHAR(255) NOT NULL,
    author_site VARCHAR(255) NOT NULL,
    author_gravatar varchar(255),
    content TEXT NOT NULL
);
INSERT INTO comment (id, url, notified, created, published,
    author_name, author_site, author_gravatar, content)
  SELECT id, url, notified, created, published,
    author_name, author_site, author_gravatar, content
  FROM _comment_old;
DROP TABLE _comment_old;
COMMIT;
PRAGMA foreign_keys = ON;
"""

cursor.executescript(script)
connection.close()
