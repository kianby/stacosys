#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import logging
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
from app.interface import api
from app.interface import form
from app.interface import report
#from app.controllers import mail
from app.interface import zclient
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

# start broker client
zclient.start()

# start processor
template_path = os.path.abspath(os.path.join(current_path, 'templates'))
processor.start(template_path)

# less feature in private mode
if not config.PRIVATE:
    # enable CORS
    cors = CORS(app, resources={r"/comments/*": {"origins": "*"}})
    from app.controllers import reader
    logger.debug('imported: %s ' % reader.__name__)

# tune logging level
if not config.DEBUG:
    logging.getLogger('app.cors').level = logging.WARNING
    logging.getLogger('werkzeug').level = logging.WARNING

logger.info("Start Stacosys application")

if __name__ == '__main__':

    app.run(host=config.HTTP_ADDRESS,
            port=config.HTTP_PORT,
            debug=config.DEBUG, use_reloader=False)
