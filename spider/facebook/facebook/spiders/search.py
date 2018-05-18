#!/usr/bin/env python
# encoding: utf-8
import time

import re

import subprocess

import os
from scrapy import Spider, Request, signals
from scrapy.conf import settings
from facebook.items import PostItem
import pymongo


class SearchPost(Spider):
    name = 'search'
    allowed_domains = ['facebook.com']
    host = 'https://m.facebook.com'
    retry_times = 0

    page_cnt = 0

    def __init__(self, keyword):
        self.keyword = keyword
        self.url = 'https://m.facebook.com/graphsearch/str/{}/stories-keyword'.format(keyword)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SearchPost, cls).from_crawler(crawler, *args, **kwargs)
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
        self.logger.info('current keyword %s', self.keyword)
        yield Request(self.url, callback=self.parse)

    def parse(self, response):
        if self.retry_times >= 3:
            self.logger.warning('重试超过3次，已自动停止重试')
            self.logger.warning('当前url: %s', response.url)
            return

        post_nodes = response.xpath('//div[@data-ft=\'{"tn":"*W"}\']')

        if not post_nodes:
            self.logger.warning('等待3分钟后重试...')
            time.sleep(60 * 3)  # 被封自动延迟3分钟再重试
            self.retry_times += 1
            yield Request(response.url, callback=self.parse, dont_filter=True)
            return

        for post_node in post_nodes:
            post_item = PostItem()
            user_data = post_node.xpath('..//td')
            post_item['avatar_url'] = user_data[0].xpath('.//img/@src').extract_first()
            post_item['user_url'] = self.host + user_data[1].xpath('.//a/@href').extract_first()
            post_item['user_name'] = user_data[1].xpath('.//a/text()').extract_first()
            post_item['post'] = post_node.xpath('string(..//div[@data-ft=\'{"tn":"*s"}\'])').extract_first()
            if post_item['post'][-4:] == '查看翻译':
                post_item['post'] = post_item['post'][:-4]

            post_item['video_urls'] = post_node.xpath('..//a[@data-ft=\'{"tn":"F"}\']/@href').extract()
            post_item['video_urls'] = list(
                map(lambda url: self.host + url if url[0] == '/' else url, post_item['video_urls']))
            post_item['img_urls'] = post_node.xpath('..//div[@data-ft=\'{"tn":"E"}\']//img/@src').extract()
            post_item['date_time'] = post_node.xpath('./div[1]/abbr/text()').extract_first()
            post_item['like_num'] = post_node.xpath('./div[2]/span[1]/a[1]/text()').extract_first()
            comments_num = post_node.xpath('./div[2]/a[1]/text()').extract_first()
            comments_num = re.search('(\d+)', comments_num)
            if comments_num:
                post_item['comments_num'] = comments_num.group(0)
            else:
                post_item['comments_num'] = '0'
            post_item['url'] = self.host + post_node.xpath('./div[2]/a[last()]/@href').extract_first()
            post_item['_id'] = post_item['url'][:100]
            yield post_item

        next_page = response.xpath('//div[@id="see_more_pager"]/a/@href').extract_first()

        if next_page and self.page_cnt <= 10:
            self.page_cnt += 1
            yield Request(url=next_page, callback=self.parse, dont_filter=True)
