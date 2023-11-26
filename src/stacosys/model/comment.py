#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    id: int = 0
    url: str = ""
    created: Optional[datetime] = None
    notified: Optional[datetime] = None
    published: Optional[datetime] = None
    author_name: str = ""
    author_site: str = ""
    author_gravatar: str = ""
    content: str = ""
