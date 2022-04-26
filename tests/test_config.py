#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from stacosys.conf.config import Config, ConfigParameter

EXPECTED_DB_SQLITE_FILE = "db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_LANG = "fr"


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.conf = Config()
        self.conf.put(ConfigParameter.DB_SQLITE_FILE, EXPECTED_DB_SQLITE_FILE)
        self.conf.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)

    def test_exists(self):
        self.assertTrue(self.conf.exists(ConfigParameter.DB_SQLITE_FILE))

    def test_get(self):
        self.assertEqual(
            self.conf.get(ConfigParameter.DB_SQLITE_FILE), EXPECTED_DB_SQLITE_FILE
        )
        self.assertEqual(self.conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertIsNone(self.conf.get(ConfigParameter.HTTP_HOST))
        self.assertEqual(self.conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertEqual(self.conf.get_int(ConfigParameter.HTTP_PORT), 8080)
        try:
            self.conf.get_bool(ConfigParameter.DB_SQLITE_FILE)
            self.assertTrue(False)
        except AssertionError:
            pass

    def test_put(self):
        self.assertFalse(self.conf.exists(ConfigParameter.LANG))
        self.conf.put(ConfigParameter.LANG, EXPECTED_LANG)
        self.assertTrue(self.conf.exists(ConfigParameter.LANG))
        self.assertEqual(self.conf.get(ConfigParameter.LANG), EXPECTED_LANG)
