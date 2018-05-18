#!/usr/bin/env python
# encoding: utf-8
import pymongo
import re
from scrapy import Spider, Request, signals
from weibo.spiders.parse import tweet
from scrapy.conf import settings
import subprocess
import os


class WeiboSearch(Spider):
    name = 'search'
    host = 'https://weibo.cn'

    def __init__(self, keyword):
        self.keyword = keyword

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(WeiboSearch, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_close, signals.spider_closed)
        return spider

    def spider_close(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client['web']
        collection = db['jobs']
        jobid = settings['DBNAME']
        job = collection.find_one({'_id': int(jobid)})
        M = job['M']
        N = job['N']
        command = 'scrapy crawl person -a M={} -a N={} -a job_id={} -s LOG_FILE=log/{}.log -s DBNAME={} -s CNAME={}'.format(
            M, N, jobid, jobid, jobid, 'person'
        )
        self.logger.info(command)
        p = subprocess.Popen([command], cwd=os.getcwd(), shell=True)
        self.logger.info(os.getcwd())
        job['pid'] = p.pid
        job['status'] = 'running-person'
        collection.save(job)

    def start_requests(self):
        self.logger.info('current keyword {}'.format(self.keyword))
        url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime=20180101&endtime=20180501&sort=time&page=1'.format(
            self.keyword)
        yield Request(url, callback=self.parse_tweet)

    def parse_tweet(self, response):
        tweet_items, next_url = tweet(response)
        for tweet_item in tweet_items:
            yield tweet_item
        if next_url:
            page_num = re.search(r'page=(\d+)', str(next_url)).group(1)
            if int(page_num) <= 2:
                yield Request(url=self.host + next_url[0], callback=self.parse_tweet, dont_filter=True)
