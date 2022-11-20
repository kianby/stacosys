#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import smtplib
import ssl
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(
        self,
        smtp_host,
        smtp_port,
        smtp_login,
        smtp_password,
        site_admin_email,
    ):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_login = smtp_login
        self._smtp_password = smtp_password
        self._site_admin_email = site_admin_email

    def send(self, subject, message):
        sender = self._smtp_login
        receivers = [self._site_admin_email]

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = self._site_admin_email
        msg["From"] = sender

        context = ssl.create_default_context()
        # TODO catch SMTP failure 
        with smtplib.SMTP_SSL(
            self._smtp_host, self._smtp_port, context=context
        ) as server:
            server.login(self._smtp_login, self._smtp_password)
            server.send_message(msg, sender, receivers)
        return True
