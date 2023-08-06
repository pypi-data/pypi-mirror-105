import sys
import time
import signal
import logging
import pickle

from scrapy.http import Request
from . import connection, defaults
from .queue import RabbitMQ

logger = logging.getLogger(__name__)


class RabbitMQScheduler(object):
    """ A RabbitMQ Scheduler for Scrapy. """
    queue = None
    stats = None

    def __init__(self, connection_url, *args, **kwargs):
        self.connection_url = connection_url
        self.waiting = False
        self.closing = False

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_settings(cls, settings):
        rabbitmq_url = settings.get('RABBITMQ_CONNECTION_PARAMETERS') or defaults.RABBITMQ_CONNECTION_PARAMETERS
        return cls(rabbitmq_url)

    @classmethod
    def from_crawler(cls, crawler):
        scheduler = cls.from_settings(crawler.settings)
        scheduler.stats = crawler.stats
        return scheduler

    def open(self, spider):

        if not hasattr(spider, 'queue_name'):
            msg = 'Please set queue_name parameter to spider. '
            raise ValueError(msg)

        self.spider = spider
        self.queue = RabbitMQ(connection_url=self.connection_url, exchange=spider.exchange,
                              queue_name=spider.queue_name, spider=spider)
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))

    def on_sigint(self, signal, frame):
        self.closing = True

    def close(self, reason):
        self.queue.close()

    def enqueue_request(self, request):
        """ Enqueues request to main queues back
        """
        if self.queue is not None:
            if self.stats:
                self.stats.inc_value('scheduler/enqueued/rabbitmq',
                                     spider=self.spider)
            self.queue.push(request)
        return True

    def next_request(self):
        """ Creates and returns a request to fire
        """
        if self.closing:
            self.close('user close')
            return

        auto_ack = True if self.spider.settings.get(
            'RABBITMQ_CONFIRM_DELIVERY', True) is False else False
        method, properties, body = self.queue.pop(auto_ack=auto_ack)

        if any([method, properties, body]):
            self.waiting = False
            if self.stats:
                self.stats.inc_value('scheduler/dequeued/rabbitmq',
                                     spider=self.spider)
            if hasattr(self.spider, "_make_request"):
                request = self.spider._make_request(method, properties, body)
            else:
                request = Request(url=body)
            if self.spider.settings.get('RABBITMQ_CONFIRM_DELIVERY', True):
                request.meta['delivery_tag'] = method.delivery_tag

            logger.info('Running request {}'.format(request.url))
            return request
        else:
            if not self.waiting:
                msg = 'Queue {} is empty. Waiting for messages...'
                self.waiting = True
                logger.info(msg.format(self.queue.queue_name))
            return None

    def ack_message(self, delivery_tag):
        if self.queue:
            self.queue.ack(delivery_tag)

    def has_pending_requests(self):
        return not self.closing
