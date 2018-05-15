#!/usr/bin/env python
# encoding: utf-8
import time
from scrapy import Spider, Request

from facebook.items import PersonFriendItem


class PersonFriend(Spider):
    name = 'person_friend'
    allowed_domains = ['facebook.com']
    host = 'https://m.facebook.com'
    username = 'andrew'
    user_url = 'https://m.facebook.com/{}'.format(username)
    url = 'https://m.facebook.com/{}/friends'.format(username)

    def start_requests(self):
        self.logger.info('current person %s', self.username)
        yield Request(self.url, callback=self.parse)

    def parse(self, response):

        friend_nodes = response.xpath('//div[@id="root"]/div/h3/following-sibling::div[1]//tr')
        for friend_node in friend_nodes:
            item = PersonFriendItem()
            item["user_url"] = self.user_url
            item["friend_name"] = friend_node.xpath('./td[2]/a/text()').extract_first()
            item["friend_url"] = self.host + friend_node.xpath('./td[2]/a/@href').extract_first()
            item["_id"] = self.user_url + "_" + item["friend_url"]
            yield item

        next_page = self.host + response.xpath('//div[@id="m_more_friends"]/a/@href').extract_first()
        if next_page:
            yield Request(next_page, callback=self.parse)
