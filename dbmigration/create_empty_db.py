#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

# What script performs: 
# - first, remove site table: crash here if table doesn't exist (compatibility test without effort)
# - remove site_id colum from comment table
script = """
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
, ulid INTEGER);
"""

cursor.executescript(script)
connection.close()