#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import smtplib
from email.mime.text import MIMEText

from stacosys.core import imap

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(
        self,
        imap_host,
        imap_port,
        imap_ssl,
        imap_login,
        imap_password,
        smtp_host,
        smtp_port,
        smtp_starttls,
        smtp_ssl,
        smtp_login,
        smtp_password,
    ):
        self._imap_host = imap_host
        self._imap_port = imap_port
        self._imap_ssl = imap_ssl
        self._imap_login = imap_login
        self._imap_password = imap_password
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_starttls = smtp_starttls
        self._smtp_ssl = smtp_ssl
        self._smtp_login = smtp_login
        self._smtp_password = smtp_password

    def _open_mailbox(self):
        return imap.Mailbox(
            self._imap_host,
            self._imap_port,
            self._imap_ssl,
            self._imap_login,
            self._imap_password,
        )

    def fetch(self):
        msgs = []
        try:
            with self._open_mailbox() as mbox:
                count = mbox.get_count()
                for num in range(count):
                    msgs.append(mbox.fetch_message(num + 1))
        except Exception:
            logger.exception("fetch mail exception")
        return msgs

    def send(self, to_email, subject, message):

        # Create the container (outer) email message.
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = to_email
        msg["From"] = self._smtp_login

        success = True
        try:
            if self._smtp_ssl:
                s = smtplib.SMTP_SSL(self._smtp_host, self._smtp_port)
            else:
                s = smtplib.SMTP(self._smtp_host, self._smtp_port)            
            if self._smtp_starttls:
                s.starttls()
            s.login(self._smtp_login, self._smtp_password)
            s.send_message(msg)
            s.quit()
        except Exception:
            logger.exception("send mail exception")
            success = False
        return success

    def delete(self, id):
        try:
            with self._open_mailbox() as mbox:
                mbox.delete_message(id)
        except Exception:
            logger.exception("delete mail exception")
