#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPException

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(self) -> None:
        self._smtp_host = ""
        self._smtp_port = 0
        self._smtp_login = ""
        self._smtp_password = ""
        self._site_admin_email = ""

    def configure_smtp(
        self, smtp_host: str, smtp_port: int, smtp_login: str, smtp_password: str
    ) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_login = smtp_login
        self._smtp_password = smtp_password

    def configure_destination(self, site_admin_email: str) -> None:
        self._site_admin_email = site_admin_email

    def check(self) -> bool:
        try:
            with SMTP_SSL(self._smtp_host, self._smtp_port) as server:
                server.login(self._smtp_login, self._smtp_password)
            return True
        except SMTPAuthenticationError:
            logger.exception("Invalid credentials")
            return False

    def send(self, subject: str, message: str) -> bool:
        sender = self._smtp_login

        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = self._site_admin_email

            with SMTP_SSL(self._smtp_host, self._smtp_port) as server:
                try:
                    server.login(self._smtp_login, self._smtp_password)
                except SMTPAuthenticationError:
                    logger.exception("Invalid credentials")
                    return False

                server.send_message(msg)
            return True
        except SMTPException:
            logger.error("Error sending email", exc_info=True)
        return False
