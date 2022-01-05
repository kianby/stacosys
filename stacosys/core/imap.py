#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import datetime
import email
import imaplib
import logging
import re
from email.message import Message

from stacosys.model.email import Attachment, Email, Part

filename_re = re.compile('filename="(.+)"|filename=([^;\n\r"\']+)', re.I | re.S)


class Mailbox(object):
    def __init__(self, host, port, ssl, login, password):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.ssl = ssl
        self.login = login
        self.password = password

    def __enter__(self):
        if self.ssl:
            self.imap = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            self.imap = imaplib.IMAP4(self.host, self.port)
        self.imap.login(self.login, self.password)
        return self

    def __exit__(self, _type, value, traceback):
        self.imap.close()
        self.imap.logout()

    def get_count(self):
        self.imap.select("Inbox")
        _, data = self.imap.search(None, "ALL")
        return sum(1 for _ in data[0].split())

    def fetch_raw_message(self, num):
        self.imap.select("Inbox")
        _, data = self.imap.fetch(str(num), "(RFC822)")
        email_msg = email.message_from_bytes(data[0][1])
        return email_msg

    def fetch_message(self, num):
        raw_msg = self.fetch_raw_message(num)

        parts = []
        attachments = []
        plain_text_content = "no plain-text part"
        for part in raw_msg.walk():
            if part.is_multipart():
                continue

            if _is_part_attachment(part):
                attachments.append(_get_attachment(part))
            else:
                try:
                    content = _to_plain_text_content(part)
                    parts.append(
                        Part(content=content, content_type=part.get_content_type())
                    )
                    if part.get_content_type() == "text/plain":
                        plain_text_content = content
                except Exception:
                    logging.exception("cannot extract content from mail part")

        return Email(
            id=num,
            encoding="UTF-8",
            date=_parse_date(raw_msg["Date"]).strftime("%Y-%m-%d %H:%M:%S"),
            from_addr=raw_msg["From"],
            to_addr=raw_msg["To"],
            subject=_email_non_ascii_to_uft8(raw_msg["Subject"]),
            parts=parts,
            attachments=attachments,
            plain_text_content=plain_text_content,
        )

    def delete_message(self, num):
        self.imap.select("Inbox")
        self.imap.store(str(num), "+FLAGS", r"\Deleted")
        self.imap.expunge()

    def delete_all(self):
        self.imap.select("Inbox")
        _, data = self.imap.search(None, "ALL")
        for num in data[0].split():
            self.imap.store(num, "+FLAGS", r"\Deleted")
            self.imap.expunge()

    def print_msgs(self):
        self.imap.select("Inbox")
        _, data = self.imap.search(None, "ALL")
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, "(RFC822)")
            self.logger.debug("Message %s\n%s\n" % (num, data[0][1]))


def _parse_date(v):
    if v is None:
        return datetime.datetime.now()
    tt = email.utils.parsedate_tz(v)
    if tt is None:
        return datetime.datetime.now()
    timestamp = email.utils.mktime_tz(tt)
    date = datetime.datetime.fromtimestamp(timestamp)
    return date


def _to_utf8(string, charset):
    return string.decode(charset).encode("UTF-8").decode("UTF-8")


def _email_non_ascii_to_uft8(string):
    # RFC 1342 is a recommendation that provides a way to represent non ASCII
    # characters inside e-mail in a way that won’t confuse e-mail servers
    subject = ""
    for v, charset in email.header.decode_header(string):
        if charset is None or charset == 'unknown-8bit':
            if type(v) is bytes:
                v = v.decode()
            subject = subject + v
        else:
            subject = subject + _to_utf8(v, charset)
    return subject


def _to_plain_text_content(part: Message) -> str:
    content = part.get_payload(decode=True)
    charset = part.get_param("charset", None)
    if charset:
        content = _to_utf8(content, charset)
    elif type(content) == bytes:
        content = content.decode("utf8")
    # RFC 3676: remove automatic word-wrapping
    return content.replace(" \r\n", " ")


def _is_part_attachment(part):
    return part.get("Content-Disposition", None)


def _get_attachment(part) -> Attachment:
    content_disposition = part.get("Content-Disposition", None)
    r = filename_re.findall(content_disposition)
    if r:
        filename = sorted(r[0])[1]
    else:
        filename = "undefined"
    content = base64.b64encode(part.get_payload(decode=True))
    content = content.decode()
    return Attachment(
        filename=_email_non_ascii_to_uft8(filename),
        content=content,
        content_type=part.get_content_type(),
    )
