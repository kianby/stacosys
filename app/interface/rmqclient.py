#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
from conf import config
from threading import Thread
import logging
import json
from core import processor
from util import rabbit

logger = logging.getLogger(__name__)

class MailConsumer(rabbit.Consumer):

    def process(self, channel, method, properties, body):
        try:
            topic = method.routing_key
            data = json.loads(body)

            if topic == 'mail.message':
                if "STACOSYS" in data['subject']:
                    logger.info('new message => {}'.format(data))
                    processor.enqueue({'request': 'new_mail', 'data': data})
                else:
                    logger.info('ignore message => {}'.format(data))
            else:
                logger.warn('unsupported message [topic={}]'.format(topic))
        except:
            logger.exception('cannot process message')


def start():
    logger.info('start rmqclient')
    #c = MessageConsumer()
    #c.start()

    credentials = pika.PlainCredentials(config.rabbitmq['username'], config.rabbitmq['password'])

    parameters = pika.ConnectionParameters(
        host=config.rabbitmq['host'], 
        port=config.rabbitmq['port'], 
        credentials=credentials, 
        virtual_host=config.rabbitmq['vhost']
    )

    connection = rabbit.Connection(parameters)
    c = MailConsumer(connection, config.rabbitmq['exchange'], 'mail.message')
    c.start()
    #print('exit rmqclient ' + str(c))