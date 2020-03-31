#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import smtplib
from email.mime.text import MIMEText

import requests

from conf import config
from core import imap
from model.email import Email

logger = logging.getLogger(__name__)


def _open_mailbox():
    return imap.Mailbox(
        config.get(config.IMAP_HOST),
        config.get_int(config.IMAP_PORT),
        config.get_bool(config.IMAP_SSL),
        config.get(config.IMAP_LOGIN),
        config.get(config.IMAP_PASSWORD),
    )


def fetch():
    msgs = []
    try:
        with _open_mailbox() as mbox:
            count = mbox.get_count()
            for num in range(count):
                msgs.append(mbox.fetch_message(num + 1))
    except:
        logger.exception("fetch mail exception")
    return msgs


def send(to_email, subject, message):

    # Create the container (outer) email message.
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["To"] = to_email
    msg["From"] = config.get(config.SMTP_LOGIN)

    success = True
    try:
        s = smtplib.SMTP(config.get(config.SMTP_HOST), config.get_int(config.SMTP_PORT))
        if config.get_bool(config.SMTP_STARTTLS):
            s.starttls()
        s.login(config.get(config.SMTP_LOGIN), config.get(config.SMTP_PASSWORD))
        s.send_message(msg)
        s.quit()
    except:
        logger.exception("send mail exception")
        success = False
    return success


def delete(id):
    try:
        with _open_mailbox() as mbox:
            mbox.delete_message(id)
    except:
        logger.exception("delete mail exception")
