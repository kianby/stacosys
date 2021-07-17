#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import unittest

from stacosys.core.templater import Templater, Template


class TemplateTestCase(unittest.TestCase):

    def get_template_content(self, lang, template_name, **kwargs):
        current_path = os.path.dirname(__file__)
        template_path = os.path.abspath(os.path.join(current_path, "../stacosys/templates"))
        template = Templater(template_path).get_template(lang, template_name)
        return template.render(kwargs)

    def test_approve_comment(self):
        content = self.get_template_content("fr", Template.APPROVE_COMMENT, original="[texte]")
        self.assertTrue(content.startswith("Bonjour,\n\nLe commentaire sera bientôt publié."))
        self.assertTrue(content.endswith("[texte]"))
        content = self.get_template_content("en", Template.APPROVE_COMMENT, original="[texte]")
        self.assertTrue(content.startswith("Hi,\n\nThe comment should be published soon."))
        self.assertTrue(content.endswith("[texte]"))

    def test_drop_comment(self):
        content = self.get_template_content("fr", Template.DROP_COMMENT, original="[texte]")
        self.assertTrue(content.startswith("Bonjour,\n\nLe commentaire ne sera pas publié."))
        self.assertTrue(content.endswith("[texte]"))
        content = self.get_template_content("en", Template.DROP_COMMENT, original="[texte]")
        self.assertTrue(content.startswith("Hi,\n\nThe comment will not be published."))
        self.assertTrue(content.endswith("[texte]"))

    def test_new_comment(self):
        content = self.get_template_content("fr", Template.NEW_COMMENT, comment="[comment]")
        self.assertTrue(content.startswith("Bonjour,\n\nUn nouveau commentaire a été posté"))
        self.assertTrue(content.endswith("[comment]\n\n--\nStacosys"))
        content = self.get_template_content("en", Template.NEW_COMMENT, comment="[comment]")
        self.assertTrue(content.startswith("Hi,\n\nA new comment has been submitted"))
        self.assertTrue(content.endswith("[comment]\n\n--\nStacosys"))

    def test_notify_message(self):
        content = self.get_template_content("fr", Template.NOTIFY_MESSAGE)
        self.assertEqual("Nouveau commentaire", content)
        content = self.get_template_content("en", Template.NOTIFY_MESSAGE)
        self.assertEqual("New comment", content)

    def test_rss_title(self):
        content = self.get_template_content("fr", Template.RSS_TITLE_MESSAGE, site="[site]")
        self.assertEqual("[site] : commentaires", content)
        content = self.get_template_content("en", Template.RSS_TITLE_MESSAGE, site="[site]")
        self.assertEqual("[site] : comments", content)
