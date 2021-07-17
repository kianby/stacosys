#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from stacosys.conf.config import Config, ConfigParameter

EXPECTED_DB_SQLITE_FILE = "db.sqlite"
EXPECTED_HTTP_PORT = 8080
EXPECTED_IMAP_PORT = "5000"
EXPECTED_IMAP_LOGIN = "user"


class ConfigTestCase(unittest.TestCase):

    def conf(self):
        conf = Config()
        conf.put(ConfigParameter.DB_SQLITE_FILE, EXPECTED_DB_SQLITE_FILE)
        conf.put(ConfigParameter.HTTP_PORT, EXPECTED_HTTP_PORT)
        conf.put(ConfigParameter.IMAP_PORT, EXPECTED_IMAP_PORT)
        conf.put(ConfigParameter.SMTP_STARTTLS, "yes")
        conf.put(ConfigParameter.IMAP_SSL, "false")
        return conf

    def test_exists(self):
        conf = self.conf()
        self.assertTrue(conf.exists(ConfigParameter.DB_SQLITE_FILE))
        self.assertFalse(conf.exists(ConfigParameter.IMAP_HOST))

    def test_get(self):
        conf = self.conf()
        self.assertEqual(conf.get(ConfigParameter.DB_SQLITE_FILE), EXPECTED_DB_SQLITE_FILE)
        self.assertEqual(conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertIsNone(conf.get(ConfigParameter.HTTP_HOST))
        self.assertEqual(conf.get(ConfigParameter.HTTP_PORT), EXPECTED_HTTP_PORT)
        self.assertEqual(conf.get(ConfigParameter.IMAP_PORT), EXPECTED_IMAP_PORT)
        self.assertEqual(conf.get_int(ConfigParameter.IMAP_PORT), int(EXPECTED_IMAP_PORT))
        try:
            conf.get_int(ConfigParameter.HTTP_PORT)
            self.assertTrue(False)
        except Exception:
            pass
        self.assertTrue(conf.get_bool(ConfigParameter.SMTP_STARTTLS))
        self.assertFalse(conf.get_bool(ConfigParameter.IMAP_SSL))
        try:
            conf.get_bool(ConfigParameter.DB_URL)
            self.assertTrue(False)
        except Exception:
            pass

    def test_put(self):
        conf = self.conf()
        self.assertFalse(conf.exists(ConfigParameter.IMAP_LOGIN))
        conf.put(ConfigParameter.IMAP_LOGIN, EXPECTED_IMAP_LOGIN)
        self.assertTrue(conf.exists(ConfigParameter.IMAP_LOGIN))
        self.assertEqual(conf.get(ConfigParameter.IMAP_LOGIN), EXPECTED_IMAP_LOGIN)
