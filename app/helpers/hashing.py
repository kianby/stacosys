#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib
from conf import config


def salt(value):
    string = '%s%s' % (value, config.security['salt'])
    dk = hashlib.sha256(string.encode())
    return dk.hexdigest()


def md5(value):
    dk = hashlib.md5(value.encode())
    return dk.hexdigest()
