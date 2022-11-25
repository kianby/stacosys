#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from stacosys.service import config
from stacosys.service.configuration import ConfigParameter

EXPECTED_DB_SQLITE_FILE = "db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_LANG = "fr"


class ConfigTestCase(unittest.TestCase):
    def setUp(self):        
        config.put(ConfigParameter.DB_SQLITE_FILE, EXPECTED_DB_SQLITE_FILE)
        config.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)

    def test_exists(self):
        self.assertTrue(config.exists(ConfigParameter.DB_SQLITE_FILE))

    def test_get(self):
        self.assertEqual(
            config.get(ConfigParameter.DB_SQLITE_FILE), EXPECTED_DB_SQLITE_FILE
        )
        self.assertEqual(config.get(ConfigParameter.HTTP_HOST), "")
        self.assertEqual(
            config.get(ConfigParameter.HTTP_PORT), str(EXPECTED_HTTP_PORT)
        )
        self.assertEqual(config.get_int(ConfigParameter.HTTP_PORT), 8080)
        try:
            config.get_bool(ConfigParameter.DB_SQLITE_FILE)
            self.assertTrue(False)
        except AssertionError:
            pass

    def test_put(self):
        self.assertFalse(config.exists(ConfigParameter.LANG))
        config.put(ConfigParameter.LANG, EXPECTED_LANG)
        self.assertTrue(config.exists(ConfigParameter.LANG))
        self.assertEqual(config.get(ConfigParameter.LANG), EXPECTED_LANG)
