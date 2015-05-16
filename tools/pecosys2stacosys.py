#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import re
import logging
import datetime
from clize import clize, run

# add necessary directories to PATH
current_path = os.path.realpath('.')
parent_path = os.path.abspath(os.path.join(current_path, '..'))
paths = [current_path, parent_path]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# import database models 
from app.services.database import provide_db
from app.helpers.hashing import salt
from app.models.site import Site
from app.models.comment import Comment

# configure logging
level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# regex
regex = re.compile(r"(\w+):\s*(.*)")

def remove_from_string(line, start):
    if line[:len(start)] == start:
        line = line[len(start):].strip()
    return line

def convert_comment(db, site, root_url, filename):
    logger.info('convert %s' % filename)
    d = {}
    content = ''
    with open(filename) as f:
        for line in f:
            match = regex.match(line)
            if match:
                d[match.group(1)] = match.group(2)
            else:
                break
        is_header = True
        for line in f:
            if is_header:
                if line.strip():
                    is_header = False
                else:
                    continue
            content = content + line

    # create DB record
    comment = Comment(site=site, author_name=d['author'], content=content)
    if 'email' in d:
        comment.author_email = d['email'].strip()
    if 'site' in d:
        comment.author_site = d['site'].strip()
    if 'url' in d:
        url = remove_from_string(d['url'], 'https://')
        url = remove_from_string(url, 'http://')
        url = remove_from_string(url, root_url)
        comment.url = remove_from_string(url, '/')
    # else:
    #    comment.url = d['article']
    if 'date' in d:
        pub = datetime.datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S')
        comment.created = pub
        comment.published = pub
    comment.save()


@provide_db
def convert(db, site_name, url, admin_email, comment_dir):

    # create DB tables if needed
    db.create_tables([Site, Comment], safe=True)

    # delete site record
    try:
        site = Site.select().where(Site.name == site_name).get()
        site.delete_instance(recursive=True)
    except Site.DoesNotExist:
        pass

    site = Site.create(name=site_name, url=url, token=salt(url), 
                       admin_email=admin_email)

    for dirpath, dirs, files in os.walk(comment_dir):
        for filename in files:
            if filename.endswith(('.md',)):
                comment_file = '/'.join([dirpath, filename])
                convert_comment(db, site, url, comment_file)
            else:
                logger.warn('ignore file %s' % filename)


@clize
def pecosys2stacosys(site, url, admin_email, comment_dir):
    convert(site, url, admin_email, comment_dir)


if __name__ == '__main__':
    run(pecosys2stacosys)
