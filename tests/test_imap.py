#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import unittest

from stacosys.core.imap import _to_utf8, _email_non_ascii_to_uft8
from email.header import Header


class ImapTestCase(unittest.TestCase):

    def test_utf8_decode(self):
        h = Header(s="Chez Darty vous avez re\udcc3\udca7u un nouvel aspirateur Vacuum gratuit jl8nz",
                   charset="unknown-8bit")
        decoded = _email_non_ascii_to_uft8(h)
        self.assertEqual(decoded, "Chez Darty vous avez reçu un nouvel aspirateur Vacuum gratuit jl8nz")
