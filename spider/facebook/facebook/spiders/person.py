#!/usr/bin/env python
# encoding: utf-8
import time
import re
import datetime
from pprint import pprint

import pymongo
from scrapy import Spider, Selector, Request
from scrapy.conf import settings

from facebook.items import PersonItem, PostItem, PersonFriendItem, CommentItem


class PersonInfoSpider(Spider):
    name = 'person'
    allowed_domains = ['facebook.com']
    host = 'https://m.facebook.com'
    post_page_counter = dict()
    friends_page_counter = dict()
    commit_page_counter = dict()

    def __init__(self, N, M):
        self.N = int(N)
        self.M = int(M)

    def start_requests(self):
        self.logger.info('starting')
        client = pymongo.MongoClient("localhost", 27017)
        posts = client[settings['DBNAME']]['Tweets_search'].find().limit(self.N)
        for post in posts:
            prefix = self.get_url_prefix(post['user_url'])
            url = "{}about".format(prefix)
            yield Request(url=url, callback=self.parse_information, meta={'level': 0, 'prefix': prefix})

    def parse_information(self, response):
        """ 抓取个人信息 """
        person_item = PersonItem()
        person_item['name'] = response.xpath('//strong[@class="bp"]/text()').extract_first()
        person_item['job_name'] = response.xpath(
            '//div[@id="work"]/div/div[2]/div[1]/div/div[1]/div[2]/span/text()').extract_first()
        person_item['job_time'] = response.xpath(
            '//div[@id="work"]/div/div[2]/div[1]/div/div[1]/div[3]/span/text()').extract_first()
        person_item['school_name'] = response.xpath(
            'string(//div[@id="education"]/div/div[2]/div[1]/div/div[1]/div[1])').extract_first()
        person_item['school_subject'] = response.xpath(
            'string(//div[@id="education"]/div/div[2]/div[1]/div/div[1]/div[2])').extract_first()
        person_item['school_time'] = response.xpath(
            'string(//div[@id="education"]/div/div[2]/div[1]/div/div[1]/div[3])').extract_first()
        person_item['location'] = response.xpath(
            'string(//div[@id="living"]/div/div[2]/div[1]//td[2])').extract_first()
        person_item['hometown'] = response.xpath(
            'string(//div[@id="living"]/div/div[2]/div[2]//td[2])').extract_first()
        person_item['contact'] = response.xpath(
            'string(//div[@id="contact-info"]/div/div[2])').extract_first()
        person_item['sex'] = response.xpath('string(//div[@title="性别"]//td[2])').extract_first()
        person_item['birthday'] = response.xpath('string(//div[@title="生日"]//td[2])').extract_first()
        person_item['relationship'] = response.xpath(
            'string(//div[@id="relationship"]/div/div[2])').extract_first()
        prefix = response.meta['prefix']
        person_item['_id'] = prefix
        yield person_item

        yield Request(url='{}timeline'.format(prefix), callback=self.parse_preson_post,
                      meta={'prefix': prefix})
        yield Request(url='{}friends'.format(prefix), callback=self.parse_friends, meta=response.meta,
                      dont_filter=True)

    def parse_preson_post(self, response):

        post_nodes = response.xpath('//div[@id="recent"]/div/div/div')
        prefix = response.meta['prefix']

        for post_node in post_nodes:
            post_item = PostItem()
            post_item['user_url'] = prefix
            post_item['user_name'] = post_node.xpath('string(./div[1]/div[1]//strong)').extract_first()
            post_item['post'] = post_node.xpath('string(./div[1]/div[2])').extract_first()
            if post_item['post'][-4:] == '查看翻译':
                post_item['post'] = post_item['post'][:-4]
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
            yield Request(url=post_item['url'], callback=self.parse_comment, meta={'post_url': post_item['url']})

        if response.xpath('//div[@id="recent"]/../div[2]/a/text()').extract_first() == '更多':
            next_page = self.host + response.xpath('//div[@id="recent"]/../div[2]/a/@href').extract_first()
            if next_page:
                if prefix in self.post_page_counter.keys():
                    self.post_page_counter[prefix] += 1
                else:
                    self.post_page_counter[prefix] = 1
                if self.post_page_counter[prefix] <= 10:
                    yield Request(url=next_page, callback=self.parse_preson_post, dont_filter=True,
                                  meta={'prefix': prefix})

    def get_url_prefix(self, user_url):
        if 'https://m.facebook.com/profile.php' in user_url:
            prefix = re.search('https://m\.facebook\.com/profile\.php\?id=\d+', user_url)
            if prefix:
                return prefix.group(0) + '&v='
            else:
                return
        else:
            prefix = re.search('(https://m.facebook.com/.*?)[?/]', user_url)
            if prefix:
                return prefix.group(1) + '?v='
            else:
                prefix = re.search('https://m.facebook.com/.*', user_url)
                if prefix:
                    return prefix.group(0) + '?v='
                else:
                    return

    def parse_friends(self, response):
        prefix = response.meta['prefix']
        friend_nodes = response.xpath('//div[@id="root"]/div/h3/following-sibling::div[1]//tr')
        for friend_node in friend_nodes:
            item = PersonFriendItem()
            item["user_url"] = prefix
            item["friend_name"] = friend_node.xpath('./td[2]/a/text()').extract_first()
            item["friend_url"] = self.host + friend_node.xpath('./td[2]/a/@href').extract_first()
            item["_id"] = prefix + "_" + item["friend_url"]
            yield item
            if response.meta['level'] < self.M:
                yield Request(url="{}about".format(prefix), callback=self.parse_information,
                              meta={'level': response.meta['level'] + 1, 'prefix': prefix})

        next_page = response.xpath('//div[@id="m_more_friends"]/a/@href').extract_first()
        if next_page:
            next_page = self.host + next_page
            if prefix in self.friends_page_counter.keys():
                self.friends_page_counter[prefix] += 1
            else:
                self.friends_page_counter[prefix] = 1
            if self.friends_page_counter[prefix] <= 3:
                yield Request(next_page, callback=self.parse_friends, dont_filter=True, meta=response.meta)

    def parse_comment(self, response):

        post_url = response.meta['post_url']

        comment_nodes = response.xpath('//div[@data-ft=\'{"tn":"R"}\']')

        for comment_node in comment_nodes:
            comment_item = CommentItem()
            comment_item['content'] = comment_node.xpath('string(./div[1])').extract_first()
            comment_item['username'] = comment_node.xpath('string(./h3)').extract_first()
            comment_item['user_url'] = self.host + comment_node.xpath('./h3/a/@href').extract_first()
            comment_item['datetime'] = comment_node.xpath('./div[3]/abbr/text()').extract_first()
            comment_item['_id'] = comment_node.xpath('../@id').extract_first() + '_' + post_url[:150]
            yield comment_item

        next_page = response.xpath('//div[starts-with(@id,"see_next")]/a/@href').extract_first()
        if next_page:
            next_page = self.host + next_page
            if post_url in self.commit_page_counter.keys():
                self.commit_page_counter[post_url] += 1
            else:
                self.commit_page_counter[post_url] = 1
            if self.commit_page_counter[post_url] <= 3:
                yield Request(url=next_page, callback=self.parse_comment, dont_filter=True, meta={'post_url': post_url})
