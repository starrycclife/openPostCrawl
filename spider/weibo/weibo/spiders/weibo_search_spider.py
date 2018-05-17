#!/usr/bin/env python
# encoding: utf-8
from scrapy import Spider, Request
from weibo.items import TweetsItem
from weibo.spiders.parse import tweet
from scrapy import settings


class WeiboSearch(Spider):
    name = 'search'
    host = 'https://weibo.cn'

    def __init__(self, keyword):
        self.keyword = keyword

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
            yield Request(url=self.host + next_url[0], callback=self.parse_tweet, dont_filter=True)
