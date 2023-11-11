#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os
import sys

from stacosys.db import database
from stacosys.interface import api, app, form
from stacosys.interface.web import admin
from stacosys.service import config, mailer, rss
from stacosys.service.configuration import ConfigParameter


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

    # check config file exists
    if not os.path.isfile(config_pathname):
        logger.error("Configuration file '%s' not found.", config_pathname)
        sys.exit(1)

    # load and check config
    config.load(config_pathname)
    is_config_ok, erreur_config = config.check()
    if not is_config_ok:
        logger.error("Configuration incorrecte '%s'", erreur_config)
        sys.exit(1)
    logger.info(config)

    # initialize database
    database.configure(config.get(ConfigParameter.DB))

    logger.info("Start Stacosys application")

    # generate RSS
    rss.configure(
        config.get(ConfigParameter.RSS_FILE),
        config.get(ConfigParameter.SITE_NAME),
        config.get(ConfigParameter.SITE_PROTO),
        config.get(ConfigParameter.SITE_URL),
    )
    rss.generate()

    # configure mailer
    mailer.configure_smtp(
        config.get(ConfigParameter.SMTP_HOST),
        config.get_int(ConfigParameter.SMTP_PORT),
        config.get(ConfigParameter.SMTP_LOGIN),
        config.get(ConfigParameter.SMTP_PASSWORD),
    )
    mailer.configure_destination(config.get(ConfigParameter.SITE_ADMIN_EMAIL))
    mailer.check()

    logger.info("start interfaces %s %s %s", api, form, admin)

    # start Flask
    app.run(
        host=config.get(ConfigParameter.HTTP_HOST),
        port=config.get_int(ConfigParameter.HTTP_PORT),
        debug=False,
        use_reloader=False,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="config path name")
    args = parser.parse_args()
    stacosys_server(args.config)
