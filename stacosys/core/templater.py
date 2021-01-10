#!/usr/bin/env python
# -*- coding: utf-8 -*-


from jinja2 import Environment, FileSystemLoader


class Templater:
    def __init__(self, template_path):
        self._env = Environment(loader=FileSystemLoader(template_path))

    def get_template(self, lang, name):
        return self._env.get_template(lang + "/" + name + ".tpl")


class Template:
    DROP_COMMENT = "drop_comment"
    APPROVE_COMMENT = "approve_comment"
    NEW_COMMENT = "new_comment"
    NOTIFY_MESSAGE = "notify_message"
    RSS_TITLE_MESSAGE = "rss_title_message"

