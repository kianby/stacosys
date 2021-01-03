#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import pytest

from stacosys.core.templater import Templater, TEMPLATE_APPROVE_COMMENT

@pytest.fixture
def templater_fr():
    current_path = os.path.dirname(__file__)
    template_path = os.path.abspath(os.path.join(current_path, "../stacosys/templates"))
    return Templater("fr", template_path)

def test_approve_comment_fr(templater_fr):
    template = templater_fr.get_template(TEMPLATE_APPROVE_COMMENT)
    assert template
    content = template.render(original="texte original")
    assert content.startswith("Bonjour,\n\nLe commentaire sera bientôt publié.")
    assert content.endswith("texte original")
