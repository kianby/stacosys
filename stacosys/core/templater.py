#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from jinja2 import Environment, FileSystemLoader


current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
env = Environment(loader=FileSystemLoader(template_path))

TEMPLATE_DROP_COMMENT = "drop_comment"
TEMPLATE_APPROVE_COMMENT = "approve_comment"
TEMPLATE_NEW_COMMENT = "new_comment"

def get_template(lang, name):
    return env.get_template(lang + "/" + name + ".tpl")

class Templater:

    def __init__(self, lang, template_path):
        self._env = Environment(loader=FileSystemLoader(template_path))
        self._lang = lang

    def get_template(self, name):
        return self._env.get_template(self._lang + "/" + name + ".tpl")


