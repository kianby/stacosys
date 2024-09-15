#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import os
import sys

from stacosys.db import database
from stacosys.i18n.messages import Messages
from stacosys.interface import api, app, form
from stacosys.interface.web import admin
from stacosys.service.configuration import Config, ConfigParameter
from stacosys.service.mail import Mailer
from stacosys.service.rssfeed import Rss


# configure logging
def configure_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s] %(name)s %(levelname)s %(message)s"
    )
    logger = logging.getLogger(__name__)
    logging.getLogger("werkzeug").level = logging.WARNING
    return logger


def load_and_validate_config(config_pathname: str, logger: logging.Logger) -> Config:
    if not os.path.isfile(config_pathname):
        logger.error("Configuration file '%s' not found.", config_pathname)
        raise FileNotFoundError(f"Configuration file '{config_pathname}' not found.")

    config = Config()
    config.load(config_pathname)
    if not config.check():
        raise ValueError(f"Invalid configuration '{config_pathname}'")
    logger.info("Configuration loaded successfully.")
    return config


def configure_and_validate_mailer(config, logger):
    mailer = Mailer()
    mailer.configure_smtp(
        config.get(ConfigParameter.SMTP_HOST),
        config.get_int(ConfigParameter.SMTP_PORT),
        config.get(ConfigParameter.SMTP_LOGIN),
        config.get(ConfigParameter.SMTP_PASSWORD),
    )
    mailer.configure_destination(config.get(ConfigParameter.SITE_ADMIN_EMAIL))
    if not mailer.check():
        logger.error("Email configuration not working")
        sys.exit(1)
    return mailer


def configure_rss(config):
    rss = Rss()
    rss.configure(
        config.get(ConfigParameter.RSS_FILE),
        config.get(ConfigParameter.SITE_NAME),
        config.get(ConfigParameter.SITE_PROTO),
        config.get(ConfigParameter.SITE_URL),
    )
    rss.generate()
    return rss


def configure_localization(config):
    messages = Messages()
    messages.load_messages(config.get(ConfigParameter.LANG))
    return messages


def main(config_pathname):
    logger = configure_logging()
    config = load_and_validate_config(config_pathname, logger)
    database.configure(config.get(ConfigParameter.DB))

    logger.info("Start Stacosys application")
    rss = configure_rss(config)
    mailer = configure_and_validate_mailer(config, logger)
    messages = configure_localization(config)

    logger.info("start interfaces %s %s %s", api, form, admin)
    app.config["CONFIG"] = config
    app.config["MAILER"] = mailer
    app.config["RSS"] = rss
    app.config["MESSAGES"] = messages
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
    try:
        main(args.config)
    except Exception as e:
        logging.error("Failed to start application: %s", e)
        sys.exit(1)
