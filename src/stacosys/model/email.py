#!/usr/bin/python
# -*- coding: UTF-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Part:
    content: str
    content_type: str


@dataclass
class Attachment:
    filename: str
    content: str
    content_type: str


@dataclass
class Email:
    id: int
    encoding: str
    date: datetime
    from_addr: str
    to_addr: str
    subject: str
    parts: List[Part]
    attachments: List[Attachment]
    plain_text_content: str
