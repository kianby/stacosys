#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os
import sys

from flask import Flask
from flask_apscheduler import APScheduler

import stacosys.conf.config as config
from stacosys.core import database
from stacosys.core import rss
#from stacosys.interface import api
#from stacosys.interface import form

# configure logging
def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    root_logger.addHandler(ch)


class JobConfig(object):

    JOBS = []

    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 4}}

    def __init__(self, imap_polling_seconds, new_comment_polling_seconds):
        self.JOBS = [
            {
                "id": "fetch_mail",
                "func": "stacosys.core.cron:fetch_mail_answers",
                "trigger": "interval",
                "seconds": imap_polling_seconds,
            },
            {
                "id": "submit_new_comment",
                "func": "stacosys.core.cron:submit_new_comment",
                "trigger": "interval",
                "seconds": new_comment_polling_seconds,
            },
        ]


def stacosys_server(config_pathname):

    app = Flask(__name__)

    conf = config.Config.load(config_pathname)

    # configure logging
    logger = logging.getLogger(__name__)
    configure_logging(logging.INFO)
    logging.getLogger("werkzeug").level = logging.WARNING
    logging.getLogger("apscheduler.executors").level = logging.WARNING

    # initialize database
    db = database.Database()
    db.setup(conf.get(config.DB_URL))

    # cron email fetcher
    app.config.from_object(
        JobConfig(
            conf.get_int(config.IMAP_POLLING), conf.get_int(config.COMMENT_POLLING)
        )
    )
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    logger.info("Start Stacosys application")

    # generate RSS for all sites
    rss_manager = rss.Rss(conf.get(config.LANG), conf.get(config.RSS_FILE), conf.get(config.RSS_PROTO))
    rss_manager.generate_all()

    # start Flask
    #logger.info("Load interface %s" % api)
    #logger.info("Load interface %s" % form)

    app.run(
        host=conf.get(config.HTTP_HOST),
        port=conf.get(config.HTTP_PORT),
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config path name")
    args = parser.parse_args()
    stacosys_server(args.config)
