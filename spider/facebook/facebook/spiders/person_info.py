#!/usr/bin/env python
# encoding: utf-8
import time
from scrapy import Spider, Request

from facebook.items import PersonItem


class PersonInfoSpider(Spider):
    name = 'person_info'
    allowed_domains = ['facebook.com']
    keyword = 'tom'
    url = 'https://m.facebook.com/{}/about'.format(keyword)

    def start_requests(self):
        self.logger.info('current person %s', self.keyword)
        yield Request(self.url, callback=self.parse)

    def parse(self, response):

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
        person_item['_id'] = self.keyword
        yield person_item
