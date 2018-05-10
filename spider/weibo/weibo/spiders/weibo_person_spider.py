#!/usr/bin/env python
# encoding: utf-8
"""
根据一个用户递归爬取M层
"""
import re
import datetime
from scrapy import Spider, Selector, Request
from weibo.items import InformationItem, RelationshipsItem

from weibo.spiders.parse import tweet


class WeiboPersonSpider(Spider):
    name = 'person'
    host = 'https://weibo.cn'

    def start_requests(self):
        userid = '5341245051'
        yield Request(url=self.host + "/%s/info" % userid, callback=self.parse_information, meta={'level': 0})

    def parse_information(self, response):
        """ 抓取个人信息 """
        information_item = InformationItem()
        selector = Selector(response)
        ID = re.findall('(\d+)/info', response.url)[0]
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        nickname = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sexOrientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vipLevel = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        url = re.findall('互联网;?[：:]?(.*?);', text1)
        information_item["_id"] = ID
        if nickname and nickname[0]:
            information_item["NickName"] = nickname[0].replace(u"\xa0", "")
        if gender and gender[0]:
            information_item["Gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            information_item["Province"] = place[0]
            if len(place) > 1:
                information_item["City"] = place[1]
        if briefIntroduction and briefIntroduction[0]:
            information_item["BriefIntroduction"] = briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                information_item["Birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception:
                information_item['Birthday'] = birthday[0]  # 有可能是星座，而非时间
        if sexOrientation and sexOrientation[0]:
            if sexOrientation[0].replace(u"\xa0", "") == gender[0]:
                information_item["SexOrientation"] = "同性恋"
            else:
                information_item["SexOrientation"] = "异性恋"
        if sentiment and sentiment[0]:
            information_item["Sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vipLevel and vipLevel[0]:
            information_item["VIPlevel"] = vipLevel[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            information_item["Authentication"] = authentication[0].replace(u"\xa0", "")
        if url:
            information_item["URL"] = url[0]
        response.meta['item'] = information_item
        yield Request('https://weibo.cn/u/{}'.format(information_item['_id']), callback=self.parse_further_information,
                      meta=response.meta)

    def parse_further_information(self, response):
        text = response.text
        information_item = response.meta['item']
        Num_Tweets = re.findall('微博\[(\d+)\]', text)
        if Num_Tweets:
            information_item['Num_Tweets'] = Num_Tweets[0]
        Num_Follows = re.findall('关注\[(\d+)\]', text)
        if Num_Follows:
            information_item['Num_Follows'] = Num_Follows[0]
        Num_Fans = re.findall('粉丝\[(\d+)\]', text)
        if Num_Fans:
            information_item['Num_Fans'] = Num_Fans[0]
        yield information_item
        """
        进一步抓取微博、粉丝和关注
        """
        yield Request(url=self.host + '/{}/profile'.format(information_item['_id']), callback=self.parse_tweet)
        yield Request(url=self.host + '/{}/follow'.format(information_item['_id']), callback=self.parse_follow,
                      dont_filter=True)
        yield Request(url=self.host + '/{}/fans'.format(information_item['_id']), callback=self.parse_fans,
                      meta={'level': response.meta['level']},
                      dont_filter=True)

    def parse_tweet(self, response):
        tweet_items, next_url = tweet(response)
        for tweet_item in tweet_items:
            yield tweet_item
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse_tweet, dont_filter=True)

    def parse_follow(self, response):
        """
        抓取关注列表
        """
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="取消关注"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/follow', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item["fan_id"] = ID
            relationships_item["followed_id"] = uid
            relationships_item["_id"] = ID + '-' + uid
            yield relationships_item
        next_url = selector.xpath('//a[text()="下页"]/@href').extract()
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse_follow, dont_filter=True)

    def parse_fans(self, response):
        """
        抓取粉丝列表
        """
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="移除"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/fans', response.url)[0]
        for uid in uids:
            relationships_item = RelationshipsItem()
            relationships_item["fan_id"] = uid
            relationships_item["followed_id"] = ID
            relationships_item["_id"] = uid + '-' + ID
            yield relationships_item
            if response.meta['level'] < 2:
                yield Request(url=self.host + "/%s/info" % uid, callback=self.parse_information,
                              meta={'level': response.meta['level'] + 1})
        next_url = selector.xpath('//a[text()="下页"]/@href').extract()
        if next_url:
            yield Request(url=self.host + next_url[0], callback=self.parse_fans, meta=response.meta, dont_filter=True)