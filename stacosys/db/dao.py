#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime

from stacosys.model.comment import Comment


def notify_site_admin(comment: Comment):
    comment.notified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()


def publish(comment: Comment):
    comment.published = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    comment.save()



