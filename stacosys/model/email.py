#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime


class Part():
    content: str
    content_type: str


class Attachment():
    filename: str
    content: str
    content_type: str


class Email():
    id: int
    encoding: str
    date: datetime
    from_addr: str
    to_addr: str
    subject: str
    parts: list[Part]
    attachments: list[Attachment]
    plain_text_content: str
