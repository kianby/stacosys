#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib
import config


def salt(value):
    string = '%s%s' % (value, config.SALT)
    dk = hashlib.sha256(string.encode())
    return dk.hexdigest()


def md5(value):
    dk = hashlib.md5(value.encode())
    return dk.hexdigest()
