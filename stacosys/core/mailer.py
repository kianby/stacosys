#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
import requests
from conf import config

logger = logging.getLogger(__name__)


def fetch():
    mails = []
    r = requests.get(config.get(config.MAILER_URL) + "/mbox")
    if r.status_code == 200:
        payload = r.json()
        if payload["count"] > 0:
            mails = payload["emails"]
    return mails


def get(id):
    payload = None
    r = requests.get(config.get(config.MAILER_URL) + "/mbox/" + str(id))
    if r.status_code == 200:
        payload = r.json()
    return payload


def send(to_email, subject, message):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    msg = {"to": to_email, "subject": subject, "content": message}
    r = requests.post(
        config.get(config.MAILER_URL) + "/mbox", data=json.dumps(msg), headers=headers
    )
    if r.status_code in (200, 201):
        logger.debug("Email for %s posted" % to_email)
    else:
        logger.warn("Cannot post email for %s" % to_email)


def delete(id):
    requests.delete(config.get(config.MAILER_URL) + "/mbox/" + str(id))
