#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
from conf import config
from threading import Thread
import logging
import json
from core import processor

logger = logging.getLogger(__name__)


def process_message(chan, method, properties, body):
    topic = method.routing_key
    data = json.loads(body)

    if topic == 'mail.message':
        logger.info('new message => {}'.format(data))
        processor.enqueue({'request': 'new_mail', 'data': data})
    else:
        logger.warn('unsupported message [topic={}]'.format(topic))


class MessageConsumer(Thread):

    def run(self):

        credentials = pika.PlainCredentials(
            config.rabbitmq['username'], config.rabbitmq['password'])
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.rabbitmq['host'], port=config.rabbitmq[
                                             'port'], credentials=credentials, virtual_host=config.rabbitmq['vhost']))

        channel = connection.channel()
        channel.exchange_declare(exchange=config.rabbitmq['exchange'],
                                 exchange_type='topic')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=config.rabbitmq['exchange'],
                           queue=queue_name,
                           routing_key='mail.message')
        channel.basic_consume(process_message,
                              queue=queue_name,
                              no_ack=True)
        channel.start_consuming()

    def stop(self):
        self.loop = False


def start():
    logger.info('start rmqclient')
    c = MessageConsumer()
    c.start()
