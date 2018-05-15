#!/usr/bin/env python
# encoding: utf-8
import time

import re
from scrapy import Spider, Request
from facebook.items import PostItem


class PersonPost(Spider):
    name = 'person_post'
    allowed_domains = ['facebook.com']
    host = 'https://m.facebook.com'
    username = 'joechang117'
    user_url = 'https://m.facebook.com/{}'.format(username)
    url = 'https://m.facebook.com/{}?v=timeline'.format(username)

    def start_requests(self):
        self.logger.info('current person %s', self.username)
        yield Request(self.url, callback=self.parse)

    def parse(self, response):

        post_nodes = response.xpath('//div[@id="recent"]/div/div/div')

        for post_node in post_nodes:
            post_item = PostItem()
            # post_item['avatar_url'] = ''
            post_item['user_url'] = self.user_url
            post_item['user_name'] = post_node.xpath('string(./div[1]/div[1]//strong)').extract_first()
            post_item['post'] = post_node.xpath('string(./div[1]/div[2])').extract_first()
            # if post_item['post'][-4:] == '查看翻译':
            #     post_item['post'] = post_item['post'][:-4]
            post_item['video_urls'] = post_node.xpath('.//div[@data-ft=\'{"tn":"H"}\']/a/@href').extract()
            post_item['video_urls'] = list(filter(lambda url: 'youtube' in url, post_item['video_urls']))
            post_item['img_urls'] = post_node.xpath('./div[1]//a/img/@src').extract()
            post_item['date_time'] = post_node.xpath(
                'string(.//div[@data-ft=\'{"tn":"*W"}\']/div[1]/abbr)').extract_first()
            like_num = post_node.xpath('string(.//div[@data-ft=\'{"tn":"*W"}\']/div[2]/span/a[1])').extract_first()
            post_item['like_num'] = like_num if like_num.isdigit() else '0'
            comments_num = post_node.xpath(
                './/div[@data-ft=\'{"tn":"*W"}\']/div[2]/a[1]/text()').extract_first()
            comments_num = re.search('(\d+)', comments_num)
            if comments_num:
                post_item['comments_num'] = comments_num.group(0)
            else:
                post_item['comments_num'] = '0'
            post_item['url'] = self.host + post_node.xpath(
                './/div[@data-ft=\'{"tn":"*W"}\']/div[2]/a[3]/@href').extract_first()
            post_item['_id'] = post_item['url'][:100]
            yield post_item

        if response.xpath('//div[@id="recent"]/../div[2]/a/text()').extract_first() == '更多':
            next_page = self.host + response.xpath('//div[@id="recent"]/../div[2]/a/@href').extract_first()
            if next_page:
                yield Request(url=next_page, callback=self.parse, dont_filter=True)
