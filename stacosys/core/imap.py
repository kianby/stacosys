#!/usr/bin/env python
# -*- coding:utf-8 -*-

import base64
import datetime
import email
import imaplib
import logging
import re

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

    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()

    def get_count(self):
        self.imap.select('Inbox')
        _, data = self.imap.search(None, 'ALL')
        return sum(1 for num in data[0].split())

    def fetch_raw_message(self, num):
        self.imap.select('Inbox')
        _, data = self.imap.fetch(str(num), '(RFC822)')
        email_msg = email.message_from_bytes(data[0][1])
        return email_msg

    def fetch_message(self, num):
        raw_msg = self.fetch_raw_message(num)
        msg = {}
        msg['encoding'] = 'UTF-8'
        msg['index'] = num
        dt = parse_date(raw_msg['Date']).strftime('%Y-%m-%d %H:%M:%S')
        msg['datetime'] = dt
        msg['from'] = raw_msg['From']
        msg['to'] = raw_msg['To']
        subject = email_nonascii_to_uft8(raw_msg['Subject'])
        msg['subject'] = subject
        parts = []
        attachments = []
        for part in raw_msg.walk():
            if part.is_multipart():
                continue

            content_disposition = part.get('Content-Disposition', None)
            if content_disposition:
                # we have attachment
                r = filename_re.findall(content_disposition)
                if r:
                    filename = sorted(r[0])[1]
                else:
                    filename = 'undefined'
                content = base64.b64encode(part.get_payload(decode=True))
                content = content.decode()
                a = {
                    'filename': email_nonascii_to_uft8(filename),
                    'content': content,
                    'content-type': part.get_content_type(),
                }
                attachments.append(a)
            else:
                part_item = {}
                content = part.get_payload(decode=True)
                content_type = part.get_content_type()
                try:
                    charset = part.get_param('charset', None)
                    if charset:
                        content = to_utf8(content, charset)
                    elif type(content) == bytes:
                        content = content.decode('utf8')
                except:
                    self.logger.exception()
                # RFC 3676: remove automatic word-wrapping
                content = content.replace(' \r\n', ' ')
                part_item['content'] = content
                part_item['content-type'] = content_type
                parts.append(part_item)
        if parts:
            msg['parts'] = parts
        if attachments:
            msg['attachments'] = attachments
        return msg

    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(str(num), '+FLAGS', r'\Deleted')
        self.imap.expunge()

    def delete_all(self):
        self.imap.select('Inbox')
        _, data = self.imap.search(None, 'ALL')
        for num in data[0].split():
            self.imap.store(num, '+FLAGS', r'\Deleted')
            self.imap.expunge()

    def print_msgs(self):
        self.imap.select('Inbox')
        _, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            self.logger.debug('Message %s\n%s\n' % (num, data[0][1]))


def parse_date(v):
    if v is None:
        return datetime.datetime.now()

    tt = email.utils.parsedate_tz(v)

    if tt is None:
        return datetime.datetime.now()

    timestamp = email.utils.mktime_tz(tt)
    date = datetime.datetime.fromtimestamp(timestamp)
    return date


def to_utf8(string, charset):
    return string.decode(charset).encode('UTF-8').decode('UTF-8')


def email_nonascii_to_uft8(string):

    # RFC 1342 is a recommendation that provides a way to represent non ASCII
    # characters inside e-mail in a way that won’t confuse e-mail servers
    subject = ''
    for v, charset in email.header.decode_header(string):
        if charset is None:
            if type(v) is bytes:
                v = v.decode()
            subject = subject + v
        else:
            subject = subject + to_utf8(v, charset)
    return subject
