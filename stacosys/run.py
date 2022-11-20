#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os
import sys

from stacosys.conf.config import Config, ConfigParameter
from stacosys.core.mailer import Mailer
from stacosys.core.rss import Rss
from stacosys.db import database
from stacosys.interface import api, app, form
from stacosys.interface.web import admin


# configure logging
def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def stacosys_server(config_pathname):
    # configure logging
    logger = logging.getLogger(__name__)
    configure_logging(logging.INFO)
    logging.getLogger("werkzeug").level = logging.WARNING
    logging.getLogger("apscheduler.executors").level = logging.WARNING

    # check config file exists
    if not os.path.isfile(config_pathname):
        logger.error("Configuration file '%s' not found.", config_pathname)
        sys.exit(1)

    # load config
    conf = Config.load(config_pathname)
    is_config_ok, erreur_config = conf.check()
    if not is_config_ok:
        logger.error("Configuration incorrecte '%s'", erreur_config)
        sys.exit(1)
    logger.info(conf)

    # check database file exists (prevents from creating a fresh db)
    db_pathname = conf.get(ConfigParameter.DB_SQLITE_FILE)
    if not db_pathname or not os.path.isfile(db_pathname):
        logger.error("Database file '%s' not found.", db_pathname)
        sys.exit(1)

    # initialize database
    database.setup(db_pathname)

    logger.info("Start Stacosys application")

    # generate RSS
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
        conf.get(ConfigParameter.SITE_ADMIN_EMAIL),
    )

    # inject config parameters into flask
    app.config.update(LANG=conf.get(ConfigParameter.LANG))
    app.config.update(SITE_NAME=conf.get(ConfigParameter.SITE_NAME))
    app.config.update(SITE_URL=conf.get(ConfigParameter.SITE_URL))
    app.config.update(SITE_REDIRECT=conf.get(ConfigParameter.SITE_REDIRECT))
    app.config.update(WEB_USERNAME=conf.get(ConfigParameter.WEB_USERNAME))
    app.config.update(WEB_PASSWORD=conf.get(ConfigParameter.WEB_PASSWORD))
    app.config.update(MAILER=mailer)
    app.config.update(RSS=rss)
    logger.info("start interfaces %s %s %s", api, form, admin)

    # start Flask
    app.run(
        host=conf.get(ConfigParameter.HTTP_HOST),
        port=conf.get_int(ConfigParameter.HTTP_PORT),
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config path name")
    args = parser.parse_args()
    stacosys_server(args.config)
