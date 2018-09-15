#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import re
import PyRSS2Gen
import markdown
import json
from datetime import datetime
from threading import Thread
from queue import Queue
from model.site import Site
from model.comment import Comment
from helper.hashing import md5
from conf import config
from core import mailer


logger = logging.getLogger(__name__)
queue = Queue()
proc = None
env = None

# keep client IP in memory until classified
client_ips = {}





def get_email_metadata(message):
    # retrieve metadata reader email from email body sent by admin
    email = ""
    m = re.search(r"email:\s(.+@.+\..+)", message)
    if m:
        email = m.group(1)
    return email


