#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from stacosys.service import rss


def test_configure():
    rss.configure("comments.xml", "blog", "http", "blog.mydomain.com")
