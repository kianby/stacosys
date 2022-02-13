#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.message import EmailMessage
from logging.handlers import SMTPHandler

logger = logging.getLogger(__name__)


class Mailer:
    def __init__(
        self,
        smtp_host,
        smtp_port,
        smtp_starttls,
        smtp_ssl,
        smtp_login,
        smtp_password,
        site_admin_email,
    ):
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_starttls = smtp_starttls
        self._smtp_ssl = smtp_ssl
        self._smtp_login = smtp_login
        self._smtp_password = smtp_password
        self._site_admin_email = site_admin_email

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
            if self._smtp_login:
                s.login(self._smtp_login, self._smtp_password)
            s.send_message(msg)
            s.quit()
        except Exception:
            logger.exception("send mail exception")
            success = False
        return success

    def get_error_handler(self):
        if self._smtp_ssl:
            mail_handler = SSLSMTPHandler(
                mailhost=(
                    self._smtp_host,
                    self._smtp_port,
                ),
                credentials=(
                    self._smtp_login,
                    self._smtp_password,
                ),
                fromaddr=self._smtp_login,
                toaddrs=self._site_admin_email,
                subject="Stacosys error",
            )
        else:
            mail_handler = SMTPHandler(
                mailhost=(
                    self._smtp_host,
                    self._smtp_port,
                ),
                credentials=(
                    self._smtp_login,
                    self._smtp_password,
                ),
                fromaddr=self._smtp_login,
                toaddrs=self._site_admin_email,
                subject="Stacosys error",
            )
        mail_handler.setLevel(logging.ERROR)
        return mail_handler


class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            smtp = smtplib.SMTP_SSL(self.mailhost, self.mailport)
            msg = EmailMessage()
            msg["From"] = self.fromaddr
            msg["To"] = ",".join(self.toaddrs)
            msg["Subject"] = self.getSubject(record)
            msg["Date"] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handleError(record)
