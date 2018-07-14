#!/usr/bin/env python
# -*- coding: utf-8 - *-

import logging
import pika
import time
from threading import Thread

logger = logging.getLogger(__name__)

EXCHANGE_TYPE = "topic"
CONNECT_DELAY = 3

class Connection:

    def __init__(self, connection_parameters):
        self._connection_parameters = connection_parameters

    def open(self):

        self._connection = None
        while True:
            try:
                self._connection = pika.BlockingConnection(
                    self._connection_parameters)
                break
            except:
                time.sleep(CONNECT_DELAY)
                logger.exception('rabbitmq connection failure. try again...')
        return self._connection

    def close(self):
        self._connection.close()
        self._connection = None

    def get(self):
        return self._connection


class Consumer(Thread):

    _connector = None
    _channel = None
    _queue_name = None

    def __init__(self, connector, exchange_name, routing_key):
        Thread.__init__(self)
        self._connector = connector
        self._exchange_name = exchange_name
        self._routing_key = routing_key

    def configure(self, connection):

        self._channel = None
        while True:
            try:

                self._channel = connection.channel()
                self._channel.exchange_declare(
                    exchange=self._exchange_name, exchange_type=EXCHANGE_TYPE
                )

                result = self._channel.queue_declare(exclusive=True)
                self._queue_name = result.method.queue
                self._channel.queue_bind(
                    exchange=self._exchange_name,
                    queue=self._queue_name,
                    routing_key=self._routing_key,
                )
                break
            except:
                logger.exception('configuration failure. try again...')
                time.sleep(CONNECT_DELAY)

    def run(self):

        self._connector.open()
        self.configure(self._connector.get())
        self._channel.basic_consume(
            self.process, queue=self._queue_name, no_ack=True)
        self._channel.start_consuming()

    def process(self, channel, method, properties, body):
        raise NotImplemented
