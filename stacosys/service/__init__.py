#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .configuration import Config
from .mail import Mailer
from .rssfeed import Rss

config = Config()
mailer = Mailer()
rss = Rss()
