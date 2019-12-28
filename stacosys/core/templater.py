#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
from conf import config

current_path = os.path.dirname(__file__)
template_path = os.path.abspath(os.path.join(current_path, "../templates"))
env = Environment(loader=FileSystemLoader(template_path))


def get_template(name):
    return env.get_template(config.get(config.LANG) + "/" + name + ".tpl")
