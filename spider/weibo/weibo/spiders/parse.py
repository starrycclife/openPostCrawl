#!/usr/bin/env python
# encoding: utf-8
import re
from scrapy import Selector
from weibo.items import TweetsItem


def tweet(response):
    selector = Selector(response)
    tweet_nodes = selector.xpath('body/div[@class="c" and @id]')
    tweet_items = []
    for tweet_node in tweet_nodes:
        tweet_item = TweetsItem()
        tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href').extract_first()
        user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
        tweet_item['user_id_1'] = user_tweet_id.group(2)
        tweet_item['weibo_url_1'] = 'https://weibo.com/{}/{}'.format(tweet_item['user_id_1'],
                                                                     user_tweet_id.group(1))

        like_num = tweet_node.xpath('.//a[contains(text(),"赞")]/text()').extract_first()
        tweet_item['like_num'] = re.search('\d+', like_num).group()

        repost_num = tweet_node.xpath('.//a[contains(text(),"转发")]/text()').extract_first()
        tweet_item['repost_num'] = re.search('\d+', repost_num).group()

        comment_num = tweet_node.xpath(
            './/a[contains(text(),"评论") and not(contains(text(),"原文"))]/text()').extract_first()
        tweet_item['comment_num'] = re.search('\d+', comment_num).group()

        repost_node = tweet_node.xpath('.//span[@class="cmt"]')

        imgs_node = tweet_node.xpath('//a[text()="原图"]/@href')

        if imgs_node:
            tweet_item['imgs'] = [imgs_node[0]]

        img_group__node = tweet_node.xpath('//a[contains(text(),"组图")]/@href')

        if img_group__node:
            tweet_node['imgs_group'] = img_group__node[0]
        else:
            tweet_node['imgs_group'] = None

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
            content_2_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
            tweet_item['content_2'] = content_2_node.xpath('string(.)').extract_first()
            repost_info = tweet_node.xpath('string(./div[last()])').extract_first()
            repost_info = repost_info.replace('转发理由:', '').replace('查看图片', '')
            tweet_item['content_1'] = repost_info.split('赞')[0].strip().replace('\u200b', '')
            tweet_item['created_at_1'] = re.search(r'收藏(.*?)[来自]?', repost_info).group(1).strip()
        else:
            tweet_item['is_repost'] = False
            tweet_info_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
            tweet_info = tweet_info_node.xpath('string(.)').extract_first()
            tweet_item['content_1'] = tweet_info.strip().replace('\u200b', '').strip()
            create_time_node = tweet_node.xpath('.//span[@class="ct"]')[0]
            create_time_info = create_time_node.xpath('string(.)').extract_first()
            tweet_item['created_at_1'] = create_time_info.split('\xa0')[0].strip()
            try:
                tweet_item['tool'] = create_time_info.split('\xa0')[1].replace('来自', '').strip()
            except:
                pass
            tweet_item['_id'] = tweet_item['weibo_url_1']
            tweet_items.append(tweet_item)
    next_url = selector.xpath('//a[text()="下页"]/@href').extract()
    return tweet_items, next_url
