#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from stacosys.conf.config import Config, ConfigParameter

EXPECTED_DB_SQLITE_FILE = "db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_IMAP_PORT = "5000"
EXPECTED_IMAP_LOGIN = "user"


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.conf = Config()
        self.conf.put(ConfigParameter.DB_SQLITE_FILE, EXPECTED_DB_SQLITE_FILE)
        self.conf.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)
        self.conf.put(ConfigParameter.IMAP_PORT, EXPECTED_IMAP_PORT)
        self.conf.put(ConfigParameter.SMTP_STARTTLS, "yes")
        self.conf.put(ConfigParameter.IMAP_SSL, "false")

    def test_exists(self):
        self.assertTrue(self.conf.exists(ConfigParameter.DB_SQLITE_FILE))
        self.assertFalse(self.conf.exists(ConfigParameter.IMAP_HOST))

    def test_get(self):
        self.assertEqual(self.conf.get(ConfigParameter.DB_SQLITE_FILE), EXPECTED_DB_SQLITE_FILE)
        self.assertEqual(self.conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertIsNone(self.conf.get(ConfigParameter.HTTP_HOST))
        self.assertEqual(self.conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertEqual(self.conf.get(ConfigParameter.IMAP_PORT), EXPECTED_IMAP_PORT)
        self.assertEqual(self.conf.get_int(ConfigParameter.IMAP_PORT), int(EXPECTED_IMAP_PORT))
        self.assertEqual(self.conf.get_int(ConfigParameter.HTTP_PORT), 8080)
        self.assertTrue(self.conf.get_bool(ConfigParameter.SMTP_STARTTLS))
        self.assertFalse(self.conf.get_bool(ConfigParameter.IMAP_SSL))
        try:
            self.conf.get_bool(ConfigParameter.DB_SQLITE_FILE)
            self.assertTrue(False)
        except AssertionError:
            pass

    def test_put(self):
        self.assertFalse(self.conf.exists(ConfigParameter.IMAP_LOGIN))
        self.conf.put(ConfigParameter.IMAP_LOGIN, EXPECTED_IMAP_LOGIN)
        self.assertTrue(self.conf.exists(ConfigParameter.IMAP_LOGIN))
        self.assertEqual(self.conf.get(ConfigParameter.IMAP_LOGIN), EXPECTED_IMAP_LOGIN)
