#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_apscheduler import APScheduler
from stacosys.interface import app


class JobConfig(object):

    JOBS: list = []

    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 1}}

    def __init__(
        self,
        new_comment_polling_seconds,
        site_name,
        site_admin_email,
        mailer,
    ):
        self.JOBS = [
            {
                "id": "submit_new_comment",
                "func": "stacosys.core.cron:submit_new_comment",
                "args": [site_name, site_admin_email, mailer],
                "trigger": "interval",
                "seconds": new_comment_polling_seconds,
            },
        ]


def configure(
    comment_polling,
    site_name,
    site_admin_email,
    mailer,
):
    app.config.from_object(
        JobConfig(
            comment_polling,
            site_name,
            site_admin_email,
            mailer,
        )
    )
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
