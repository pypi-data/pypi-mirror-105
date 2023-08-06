import time
import signal
import logging
from scrapy import signals
from scrapy.exceptions import DontCloseSpider

from scrapy.http import Request
from . import connection, defaults
from .queue import RabbitMQ

logger = logging.getLogger(__name__)


class RabbitMQScheduler(object):
    """ A RabbitMQ Scheduler for Scrapy. """
    mq_client = None
    stats = None
    crawler = None
    is_closing = False
    parse_faild_times = 0
    queue_name = None

    def __init__(self, connection_url, max_idle_time, spider_parse_failed_times, *args, **kwargs):
        self.connection_url = connection_url
        self.max_idle_time = max_idle_time
        self.spider_parse_failed_times = spider_parse_failed_times

    def __len__(self):
        return len(self.mq_client)

    @classmethod
    def from_settings(cls, settings):
        rabbitmq_url = settings.get('RABBITMQ_CONNECTION_PARAMETERS') or defaults.RABBITMQ_CONNECTION_PARAMETERS
        max_idle_time = settings.get('SCHEDULER_MAX_IDLE_TIME') or defaults.SCHEDULER_MAX_IDLE_TIME
        spider_parse_failed_times = settings.get(
            'SPIDER_PARSE_FAILD_MAX_TIMES') or defaults.SPIDER_PARSE_FAILD_MAX_TIMES
        return cls(rabbitmq_url, max_idle_time, spider_parse_failed_times)

    @classmethod
    def from_crawler(cls, crawler):
        scheduler = cls.from_settings(crawler.settings)
        scheduler.crawler = crawler
        scheduler.stats = crawler.stats
        crawler.signals.connect(scheduler.closing, signal.SIGTERM)  # 接收到停止信号，不再从队列获取数据
        crawler.signals.connect(scheduler.close, signals.spider_closed)  # 关闭爬虫时关闭连接
        crawler.signals.connect(scheduler.spider_idle, signals.spider_idle)  # 最大等待时间
        crawler.signals.connect(scheduler.ack_message, signals.item_scraped)  # 保存item后发送消息确认
        crawler.signals.connect(scheduler.nack_message, signals.item_error)  # 保存item失败时，发送nack
        crawler.signals.connect(scheduler.nack_on_spider_error, signals.spider_error)  # 解析程序出错时，发送nack
        return scheduler

    def spider_idle(self) -> None:
        """"""
        working = self.schedule_next_requests()

        if working:
            self.start_idle_time = None
            raise DontCloseSpider
        else:
            if not self.start_idle_time:
                self.start_idle_time = time.time()

            if time.time() - self.start_idle_time <= self.max_idle_time:
                raise DontCloseSpider

    def schedule_next_requests(self) -> bool:
        """将从RabbitMQ中获取的任务通过 `scrapy.engine` 放入调度器的队列中.
        Returns:
            bool: 当前爬虫是否又有任务处理.
        """
        working = False

        for req in self.next_request():
            self.crawler.engine.crawl(req, spider=self)
            working = True

        return working

    def open(self, spider):
        self.spider = spider
        self.queue_name = spider.name
        self.error_queue_name = '{}_error'.format(spider.name)
        self.mq_client = RabbitMQ(connection_url=self.connection_url, exchange=spider.exchange,
                                  queue_name=self.queue_name, spider=spider)
        if len(self.mq_client):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.mq_client))

    def enqueue_request(self, request):
        """ Enqueues request to main queues back
        """
        if self.mq_client is not None:
            if self.stats:
                self.stats.inc_value('scheduler/enqueued/rabbitmq',
                                     spider=self.spider)
            self.mq_client.push(request)
        return True

    def next_request(self):
        """ Creates and returns a request to fire
        """
        if self.is_closing:
            return None
        auto_ack = True if self.spider.settings.get('RABBITMQ_CONFIRM_DELIVERY', True) is False else False
        body, channel_id = self.mq_client.pop(auto_ack=auto_ack)

        if self.stats:
            self.stats.inc_value('scheduler/dequeued/rabbitmq',
                                 spider=self.spider)
        if hasattr(self.spider, "_make_request"):
            request = self.spider._make_request(body)
        else:
            request = Request(url=body.decode('utf-8'))
        if self.spider.settings.get('RABBITMQ_CONFIRM_DELIVERY', True):
            request.meta['channel_id'] = channel_id

        logger.debug('Running request {}'.format(request.url))
        return request

    def ack_message(self, item, spider, response):
        channel_id = response.meta.get("channel_id")
        self.mq_client.ack(channel_id=channel_id)
        logger.debug('消息确认成功，item from:%s' % response.url)

    def nack_message(self, item, spider, response):
        self.mq_client.push(self.error_queue_name, response.request)
        # channel_id = response.meta.get("channel_id")
        # self.mq_client.nack(channel_id=channel_id)
        # logger.debug('消息重回队列成功，item from:%s' % response.url)

    def nack_on_spider_error(self, failure, response, spider):
        self.mq_client.push(self.error_queue_name, response.request)
        # channel_id = response.meta.get("channel_id")
        # self.mq_client.nack(channel_id=channel_id)
        # logger.debug('spider parse function failure')
        # logger.exception(failure)
        # logger.debug('消息重回队列成功，item from:%s' % response.url)
        self.parse_faild_times += 1
        if self.parse_faild_times >= self.spider_parse_failed_times:
            spider.crawler.engine.close_spider(spider=spider, reason="解析程序异常次数达到上限.")

    def has_pending_requests(self):
        return not self.closing

    def closing(self, signal, frame):
        self.is_closing = True

    def close(self, reason):
        self.mq_client.close()
        logger.info('关闭rabbitmq连接.')
