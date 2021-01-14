#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from jinja2 import Environment, FileSystemLoader


class Template(Enum):
    DROP_COMMENT = "drop_comment"
    APPROVE_COMMENT = "approve_comment"
    NEW_COMMENT = "new_comment"
    NOTIFY_MESSAGE = "notify_message"
    RSS_TITLE_MESSAGE = "rss_title_message"


class Templater:
    def __init__(self, template_path):
        self._env = Environment(loader=FileSystemLoader(template_path))

    def get_template(self, lang, template: Template):
        return self._env.get_template(lang + "/" + template.value + ".tpl")

