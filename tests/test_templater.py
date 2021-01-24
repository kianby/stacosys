#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

from stacosys.core.templater import Templater, Template


def get_template_content(lang, template_name, **kwargs):
    current_path = os.path.dirname(__file__)
    template_path = os.path.abspath(os.path.join(current_path, "../stacosys/templates"))
    templater = Templater(template_path)
    template = templater.get_template(lang, template_name)
    assert template
    return template.render(kwargs)


def test_approve_comment():
    content = get_template_content("fr", Template.APPROVE_COMMENT, original="[texte]")
    assert content.startswith("Bonjour,\n\nLe commentaire sera bientôt publié.")
    assert content.endswith("[texte]")
    content = get_template_content("en", Template.APPROVE_COMMENT, original="[texte]")
    assert content.startswith("Hi,\n\nThe comment should be published soon.")
    assert content.endswith("[texte]")


def test_drop_comment():
    content = get_template_content("fr", Template.DROP_COMMENT, original="[texte]")
    assert content.startswith("Bonjour,\n\nLe commentaire ne sera pas publié.")
    assert content.endswith("[texte]")
    content = get_template_content("en", Template.DROP_COMMENT, original="[texte]")
    assert content.startswith("Hi,\n\nThe comment will not be published.")
    assert content.endswith("[texte]")


def test_new_comment():
    content = get_template_content("fr", Template.NEW_COMMENT, comment="[comment]")
    assert content.startswith("Bonjour,\n\nUn nouveau commentaire a été posté")
    assert content.endswith("[comment]\n\n--\nStacosys")
    content = get_template_content("en", Template.NEW_COMMENT, comment="[comment]")
    assert content.startswith("Hi,\n\nA new comment has been submitted")
    assert content.endswith("[comment]\n\n--\nStacosys")


def test_notify_message():
    content = get_template_content("fr", Template.NOTIFY_MESSAGE)
    assert content == "Nouveau commentaire"
    content = get_template_content("en", Template.NOTIFY_MESSAGE)
    assert content == "New comment"


def test_rss_title():
    content = get_template_content("fr", Template.RSS_TITLE_MESSAGE, site="[site]")
    assert content == "[site] : commentaires"
    content = get_template_content("en", Template.RSS_TITLE_MESSAGE, site="[site]")
    assert content == "[site] : comments"
