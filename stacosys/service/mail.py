#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import smtplib
import ssl
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(self) -> None:
        self._smtp_host: str = ""
        self._smtp_port: int = 0
        self._smtp_login: str = ""
        self._smtp_password: str = ""
        self._site_admin_email: str = ""

    def configure_smtp(
            self,
            smtp_host,
            smtp_port,
            smtp_login,
            smtp_password,
    ) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_login = smtp_login
        self._smtp_password = smtp_password

    def configure_destination(self, site_admin_email) -> None:
        self._site_admin_email = site_admin_email

    def check(self):
        server = smtplib.SMTP_SSL(
            self._smtp_host, self._smtp_port, context=ssl.create_default_context()
        )
        server.login(self._smtp_login, self._smtp_password)
        server.close()

    def send(self, subject, message) -> bool:
        sender = self._smtp_login
        receivers = [self._site_admin_email]

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = self._site_admin_email
        msg["From"] = sender

        # pylint: disable=bare-except
        try:
            server = smtplib.SMTP_SSL(
                self._smtp_host, self._smtp_port, context=ssl.create_default_context()
            )
            server.login(self._smtp_login, self._smtp_password)
            server.send_message(msg, sender, receivers)
            server.close()
            success = True
        except:
            success = False
        return success
