#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import NamedTuple
from typing import List
from datetime import datetime


class Part(NamedTuple):
    content: str
    content_type: str


class Attachment(NamedTuple):
    filename: str
    content: str
    content_type: str


class Email(NamedTuple):
    id: int
    encoding: str
    date: datetime
    from_addr: str
    to_addr: str
    subject: str
    parts: List[Part]
    attachments: List[Attachment]
    plain_text_content: str = 'no plain-text part'
