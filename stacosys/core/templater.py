#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from jinja2 import Environment, FileSystemLoader

from stacosys.conf import config

current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
env = Environment(loader=FileSystemLoader(template_path))


def get_template(lang, name):
    return env.get_template(lang + "/" + name + ".tpl")
