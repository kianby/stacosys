#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3
import datetime
from ulid import ULID

# add column ulid
connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()
script = """
PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;
ALTER TABLE comment ADD ulid INTEGER;
COMMIT;
PRAGMA foreign_keys = ON;
"""
cursor.executescript(script)
connection.close()

# fill in ulid column
connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()
updates = []
for row in cursor.execute('SELECT * FROM comment'):
    row_id = row[0]
    string_created = row[2]
    date_created = datetime.datetime.strptime(string_created, "%Y-%m-%d %H:%M:%S")
    ulid = ULID.from_datetime(date_created)
    update = "UPDATE comment SET ulid = " + str(int(ulid)) + " WHERE id = " + str(row_id)
    print(update)
    updates.append(update)

for update in updates:
    pass
    connection.execute(update)
connection.commit()
connection.close()
