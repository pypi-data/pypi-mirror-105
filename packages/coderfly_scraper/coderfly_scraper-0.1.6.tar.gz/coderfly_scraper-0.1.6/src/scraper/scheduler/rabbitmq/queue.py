# -*- coding:utf-8 -*-
"""
@desc: 
"""
import logging

import pika
from scrapy.utils.reqser import request_to_dict

from . import connection, picklecompat

logger = logging.getLogger(__name__)


class RabbitMQ:

    def __init__(self, connection_url, queue_name, spider=None, exchange=""):
        self.connection_url = connection_url
        self.queue_name = queue_name
        self.spider = spider
        self.server = None
        self.channel = None
        self.exchange = exchange
        self.serializer = picklecompat
        self.connect()

    def __len__(self):
        """Return the length of the queue"""
        declared = self.channel.queue_declare(self.queue_name, passive=True)
        return declared.method.message_count

    def _encode_request(self, request):
        """Encode a request object"""
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)

    def push(self, request):
        if self.spider.settings.get('RABBITMQ_CONFIRM_DELIVERY', True):
            properties = pika.BasicProperties(
                delivery_mode=2,  # 消息持久化
            )
        else:
            properties = {

            }
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.queue_name,
                                   body=self._encode_request(request),
                                   properties=properties)

    def pop(self, auto_ack=False):
        return self.channel.basic_get(queue=self.queue_name, auto_ack=auto_ack)

    def ack(self, delivery_tag):
        self.channel.basic_ack(delivery_tag=delivery_tag)

    def nack(self, delivery_tag):
        self.channel.basic_nack(delivery_tag=delivery_tag, requeue=True)

    def connect(self):
        """connect to rabbitmq server and declare queue"""
        connection = pika.BlockingConnection(pika.URLParameters(self.connection_url))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=self.spider.settings.get('RABBITMQ_DURABLE', True))
        if self.spider.settings.get('RABBITMQ_CONFIRM_DELIVERY', True):
            channel.confirm_delivery()
        self.server = connection
        self.channel = channel

    def close(self):
        self.channel.close()
        logger.info('channel has closed...')
        self.server.close()
        logger.info('connection has closed....')
