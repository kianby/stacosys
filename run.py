#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import hashlib
import logging
import os
import sys

from stacosys.conf.config import Config, ConfigParameter
from stacosys.core.mailer import Mailer
from stacosys.core.rss import Rss
from stacosys.db import database
from stacosys.interface import api
from stacosys.interface import app
from stacosys.interface import form
from stacosys.interface import scheduler
from stacosys.interface.web import admin


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


def stacosys_server(config_pathname):
    # configure logging
    logger = logging.getLogger(__name__)
    configure_logging(logging.INFO)
    logging.getLogger("werkzeug").level = logging.WARNING
    logging.getLogger("apscheduler.executors").level = logging.WARNING

    # check config file exists
    if not os.path.isfile(config_pathname):
        logger.error(f"Configuration file '{config_pathname}' not found.")
        sys.exit(1)

    # initialize config
    conf = Config.load(config_pathname)
    logger.info(conf.__repr__())

    # check database file exists (prevents from creating a fresh db)
    db_pathname = conf.get(ConfigParameter.DB_SQLITE_FILE)
    if not os.path.isfile(db_pathname):
        logger.error(f"Database file '{db_pathname}' not found.")
        sys.exit(1)

    # initialize database
    db = database.Database()
    db.setup(db_pathname)

    logger.info("Start Stacosys application")

    # generate RSS for all sites
    rss = Rss(
        conf.get(ConfigParameter.LANG),
        conf.get(ConfigParameter.RSS_FILE),
        conf.get(ConfigParameter.RSS_PROTO),
        conf.get(ConfigParameter.SITE_NAME),
        conf.get(ConfigParameter.SITE_URL),
    )
    rss.generate()

    # configure mailer
    mailer = Mailer(
        conf.get(ConfigParameter.SMTP_HOST),
        conf.get_int(ConfigParameter.SMTP_PORT),
        conf.get(ConfigParameter.SMTP_LOGIN),
        conf.get(ConfigParameter.SMTP_PASSWORD),
        conf.get(ConfigParameter.SITE_ADMIN_EMAIL)
    )

    # configure scheduler
    conf.put(ConfigParameter.SITE_TOKEN, hashlib.sha1(conf.get(ConfigParameter.SITE_NAME).encode('utf-8')).hexdigest())
    scheduler.configure(
        conf.get_int(ConfigParameter.COMMENT_POLLING),
        conf.get(ConfigParameter.SITE_NAME),
        mailer,
    )

    # inject config parameters into flask
    app.config.update(LANG=conf.get(ConfigParameter.LANG))
    app.config.update(SITE_URL=conf.get(ConfigParameter.SITE_URL))
    app.config.update(SITE_REDIRECT=conf.get(ConfigParameter.SITE_REDIRECT))
    app.config.update(WEB_USERNAME=conf.get(ConfigParameter.WEB_USERNAME))
    app.config.update(WEB_PASSWORD=conf.get(ConfigParameter.WEB_PASSWORD))
    logger.info(f"start interfaces {api} {form} {admin}")

    # start Flask
    app.run(
        host=conf.get(ConfigParameter.HTTP_HOST),
        port=conf.get(ConfigParameter.HTTP_PORT),
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config path name")
    args = parser.parse_args()
    stacosys_server(args.config)
