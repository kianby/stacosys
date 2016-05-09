#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import logging
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.cors import CORS

# add current path and parent path to syspath
current_path = os.path.dirname(__file__)
parent_path = os.path.abspath(os.path.join(current_path, os.path.pardir))
paths = [current_path, parent_path]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# more imports
import config
from app.services import database
from app.services import processor
from app.controllers import api
from app.controllers import mail
from app.controllers import reader
from app import app


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

logging_level = (20, 10)[config.DEBUG]
configure_logging(logging_level)

logger = logging.getLogger(__name__)

# initialize database
database.setup()

# routes
logger.debug('imported: %s ' % api.__name__)
logger.debug('imported: %s ' % mail.__name__)
logger.debug('imported: %s ' % reader.__name__)

# start processor
template_path = os.path.abspath(os.path.join(current_path, 'templates'))
processor.start(template_path)

app.wsgi_app = ProxyFix(app.wsgi_app)

logger.info("Start Stacosys application")

# enable CORS
cors = CORS(app, resources={r"/comments/*": {"origins": "*"}})

# tune logging level
if not config.DEBUG:
    logging.getLogger('flask_cors').level = logging.WARNING
    logging.getLogger('werkzeug').level = logging.WARNING

app.run(host=config.HTTP_ADDRESS,
        port=config.HTTP_PORT,
        debug=config.DEBUG, use_reloader=False)
