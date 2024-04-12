#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from stacosys.service.rssfeed import Rss


def test_configure():
    rss = Rss()
    rss.configure("comments.xml", "blog", "http", "blog.mydomain.com")
