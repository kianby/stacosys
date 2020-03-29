#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import NamedTuple
from datetime import datetime

class Email(NamedTuple):
    id: int
    encoding: str
    date: datetime
    from_addr: str
    to_addr: str
    subject: str
    content: str
