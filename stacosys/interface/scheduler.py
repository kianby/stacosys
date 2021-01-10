#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_apscheduler import APScheduler
from stacosys.interface import app


class JobConfig(object):

    JOBS = []

    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 4}}

    def __init__(self, imap_polling_seconds, new_comment_polling_seconds, lang, site_name, site_token, site_admin_email, mailer, rss):
        self.JOBS = [
            {
                "id": "fetch_mail",
                "func": "stacosys.core.cron:fetch_mail_answers",
                "args": [lang, mailer, rss],
                "trigger": "interval",
                "seconds": imap_polling_seconds,
            },
            {
                "id": "submit_new_comment",
                "func": "stacosys.core.cron:submit_new_comment",
                "args": [lang, site_name, site_token, site_admin_email, mailer],
                "trigger": "interval",
                "seconds": new_comment_polling_seconds,
            },
        ]


def configure(imap_polling, comment_polling, lang, site_name, site_token, site_admin_email, mailer, rss):
    app.config.from_object(JobConfig(imap_polling, comment_polling, lang, site_name, site_token, site_admin_email, mailer, rss))
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
