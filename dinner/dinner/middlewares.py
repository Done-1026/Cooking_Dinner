# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals
import requests

from dinner.info import AGENTS
from dinner.proxies import Proxies


class DinnerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UserAgentDownloaderMiddleware(object):
    def process_request(self,request,spider):
        request.headers['User-Agent'] = random.choice(AGENTS)
        #print(request.headers)


class ProxyDownloaderMiddleware(object):

    def __init__(self):
        self.pool = Proxies()
        self.ip = random.choice(list(self.pool.pool))
        
    
    def process_request(self,request,spider):       
        request.meta['proxy'] = 'https://' + self.ip
        print('request ip:',self.ip)
        
    def process_response(self,request,response,spider):
        '''查看返回的状态码，如果不是200刚换ip重新请求'''
        if response.status != 200:
            self.ip = ranodm.choice(list(self.pool.pool))
            request.meta['proxy'] = 'https://' + self.ip
            print('change request ip to:',self.ip)
            return request
        return response






    
