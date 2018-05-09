#!/usr/bin/env python
# encoding: utf-8
import random
import re
from scrapy import Spider, Request, Selector

from weibo.items import TweetsItem


class WeiboSearch(Spider):
    name = 'weiboSearch'

    def start_requests(self):
        keyword = '营养早餐'
        print('current keyword {}'.format(keyword))
        for page_num in range(1, 100):
            url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime=20180301&endtime=20180401&sort=time&page={}'.format(
                keyword, page_num)
            yield Request(url, callback=self.parse_tweet)

    def parse_tweet(self, response):
        selector = Selector(response)
        tweet_nodes = selector.xpath('body/div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            tweet_item = TweetsItem()
            tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href').extract_first()
            user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
            tweet_item['user_id_1'] = user_tweet_id.group(2)
            tweet_item['weibo_url_1'] = 'https://weibo.com/{}/{}'.format(tweet_item['user_id_1'],
                                                                         user_tweet_id.group(1))
            tweet_item['name_1'] = tweet_node.xpath('.//a[@class="nk"]/text()').extract_first()
            repost_node = tweet_node.xpath('.//span[@class="cmt"]')
            if repost_node:
                repost_node = repost_node[0]
                tweet_item['is_repost'] = True
                user_url_2 = repost_node.xpath('./a/@href').extract_first()
                try:
                    tweet_item['user_id_2'] = re.search(r'u?/(\d+)$', user_url_2).group(1)
                    source_tweet_comment_url = tweet_node.xpath('.//a[contains(text(),"原文评论")]/@href').extract_first()
                    source_tweet_id = re.search(r'comment/(.*?)\?', source_tweet_comment_url).group(1)
                    tweet_item['weibo_url_2'] = 'https://weibo.com/{}/{}'.format(tweet_item['user_id_2'],
                                                                                 source_tweet_id)
                except:
                    continue
                tweet_item['name_2'] = repost_node.xpath('./a/text()').extract_first()
                content_2_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
                tweet_item['content_2'] = content_2_node.xpath('string(.)').extract_first()
                repost_info = tweet_node.xpath('string(./div[last()])').extract_first()
                repost_info = repost_info.replace('转发理由:', '').replace('查看图片', '')
                tweet_item['content_1'] = repost_info.split('赞')[0].strip().replace('\u200b', '')
                tweet_item['created_at_1'] = re.search(r'收藏(.*?)[来自]?', repost_info).group(1).strip()
            else:
                tweet_item['is_repost'] = False
                tweet_info_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
                tweet_info = tweet_info_node.xpath('string(.)').extract_first()[1:]
                tweet_item['content_1'] = tweet_info.strip().replace('\u200b', '')

                create_time_node = tweet_node.xpath('.//span[@class="ct" and contains(text(),"月")]')[0]
                create_time_info = create_time_node.xpath('string(.)').extract_first()
                tweet_item['created_at_1'] = create_time_info.split('来自')[0].strip()
            yield tweet_item
