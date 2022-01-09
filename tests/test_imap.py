#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import unittest
from email.header import Header

from stacosys.core import imap


class ImapTestCase(unittest.TestCase):

    def test_utf8_decode(self):
        h = Header(s="Chez Darty vous avez re\udcc3\udca7u un nouvel aspirateur Vacuum gratuit jl8nz",
                   charset="unknown-8bit")
        decoded = imap._email_non_ascii_to_uft8(h)
        self.assertEqual(decoded, "Chez Darty vous avez reçu un nouvel aspirateur Vacuum gratuit jl8nz")

    def test_parse_date(self):
        now = datetime.datetime.now()
        self.assertGreaterEqual(imap._parse_date(None), now)
        self.assertEqual(imap._parse_date("Wed, 8 Dec 2021 20:05:20 +0100"), datetime.datetime(2021, 12, 8, 20, 5, 20))
