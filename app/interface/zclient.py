#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from conf import config
from threading import Thread
import logging
import json
from app.services import processor

logger = logging.getLogger(__name__)

context = zmq.Context()


def process(message):
    data = json.loads(message)
    if data['topic'] == 'email:newmail':
        logger.info('newmail => {}'.format(data))
        processor.enqueue({'request': 'new_mail', 'data': data})


class Consumer(Thread):

    def run(self):
        zsub = context.socket(zmq.SUB)
        zsub.connect('tcp://127.0.0.1:{}'.format(config.zmq['pub_port']))
        zsub.setsockopt_string(zmq.SUBSCRIBE, '')
        self.loop = True
        while self.loop:
            message = zsub.recv()
            try:
                process(message)
            except:
                logger.exception('cannot process broker message')

    def stop(self):
        self.loop = False


def start():
    c = Consumer()
    c.start()
