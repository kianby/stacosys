#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import logging
from flask import Flask
from conf import config
from jsonschema import validate
from flask_apscheduler import APScheduler

app = Flask(__name__)

# add current path and parent path to syspath
current_path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(current_path, os.path.pardir))
paths = [current_path, parent_path]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# more imports
import database
import processor
from interface import api
from interface import form

# configure logging
def configure_logging(level):
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(name)s %(levelname)s %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    root_logger.addHandler(ch)

logging_level = (20, 10)[config.general['debug']]
configure_logging(logging_level)

logger = logging.getLogger(__name__)

class Config(object):
    JOBS = [
        {
            'id': 'fetch_mail',
            'func': 'core.cron:fetch_mail_answers',
            'trigger': 'interval',
            'seconds': 120
        },
        {
            'id': 'submit_new_comment',
            'func': 'core.cron:submit_new_comment',
            'trigger': 'interval',
            'seconds': 60
        },
    ]

# initialize database
database.setup()  

# start processor
template_path = os.path.abspath(os.path.join(current_path, '../templates'))
processor.start(template_path)

# cron
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# tune logging level
if not config.general['debug']:
    logging.getLogger('werkzeug').level = logging.WARNING

logger.info("Start Stacosys application")

app.run(host=config.http['host'],
        port=config.http['port'],
        debug=config.general['debug'], use_reloader=False)