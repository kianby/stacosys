#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import unittest
from email.header import Header
from email.message import Message

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
        parsed = imap._parse_date("Wed, 8 Dec 2021 20:05:20 +0100")
        self.assertEqual(parsed.day, 8)
        self.assertEqual(parsed.month, 12)
        self.assertEqual(parsed.year, 2021)
        # do not compare hours. don't care about timezone

    def test_to_plain_text_content(self):
        msg = Message()
        payload = b"non\r\n\r\nLe 08/12/2021 \xc3\xa0 20:04, kianby@free.fr a \xc3\xa9crit\xc2\xa0:\r\n> Bonjour,\r\n>\r\n> Un nouveau commentaire a \xc3\xa9t\xc3\xa9 post\xc3\xa9 pour l'article /2021/rester-discret-sur-github//\r\n>\r\n> Vous avez deux r\xc3\xa9ponses possibles :\r\n> - rejeter le commentaire en r\xc3\xa9pondant NO (ou no),\r\n> - accepter le commentaire en renvoyant cet email tel quel.\r\n>\r\n> Si cette derni\xc3\xa8re option est choisie, Stacosys publiera le commentaire tr\xc3\xa8s bient\xc3\xb4t.\r\n>\r\n> Voici les d\xc3\xa9tails concernant le commentaire :\r\n>\r\n> author: ET Rate\r\n> site:\r\n> date: 2021-12-08 20:03:58\r\n> url: /2021/rester-discret-sur-github//\r\n>\r\n> gfdgdgf\r\n>\r\n>\r\n> --\r\n> Stacosys\r\n"
        msg.set_payload(payload, "UTF-8")
        self.assertTrue(imap._to_plain_text_content(msg))
