#!/usr/bin/env python
# encoding: utf-8
import time

import re
from scrapy import Spider, Request
from facebook.items import CommentItem


class PostComment(Spider):
    name = 'post_comment'
    allowed_domains = ['facebook.com']
    host = 'https://m.facebook.com'
    url = 'https://m.facebook.com/story.php?story_fbid=2156914471001954&id=114223998604355&refid=17&_ft_' \
          '=top_level_post_id.2156914471001954%3Atl_objid.2156914471001954%3Athrowback_story_fbid.2156914471001954' \
          '%3Apage_id.114223998604355%3Apage_insights.%7B%22114223998604355%22%3A%7B%22role%22%3A1%2C%22page_id%22' \
          '%3A114223998604355%2C%22post_context%22%3A%7B%22story_fbid%22%3A2156914471001954%2C%22publish_time%22' \
          '%3A1524925081%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22object_fbtype%22%3A266%7D%2C' \
          '%22actor_id%22%3A114223998604355%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A' \
          '%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%2C%22targets%22%3A%5B%7B%22page_id%22' \
          '%3A114223998604355%2C%22actor_id%22%3A114223998604355%2C%22role%22%3A1%2C%22post_id%22%3A2156914471001954' \
          '%2C%22share_id%22%3A0%7D%5D%7D%2C%22121284336854%22%3A%7B%22page_id%22%3A121284336854%2C%22role%22%3A16%2C' \
          '%22actor_id%22%3A114223998604355%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A' \
          '%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%7D%2C%22162334690540160%22%3A%7B%22page_id%22' \
          '%3A162334690540160%2C%22role%22%3A16%2C%22actor_id%22%3A114223998604355%2C%22psn%22%3A' \
          '%22EntStatusCreationStory%22%2C%22sl%22%3A4%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22' \
          '%3A0%7D%7D%7D%3Athid.114223998604355%3A306061129499414%3A2%3A0%3A1527836399%3A1124367764008926817&__tn__' \
          '=%2AW-R#footer_action_list '

    def start_requests(self):
        self.logger.info('current url %s', self.url)
        yield Request(self.url, callback=self.parse)

    def parse(self, response):

        comment_nodes = response.xpath('//div[@data-ft=\'{"tn":"R"}\']')

        for comment_node in comment_nodes:
            comment_item = CommentItem()
            comment_item['content'] = comment_node.xpath('string(./div[1])').extract_first()
            comment_item['username'] = comment_node.xpath('string(./h3)').extract_first()
            comment_item['user_url'] = self.host + comment_node.xpath('./h3/a/@href').extract_first()
            comment_item['datetime'] = comment_node.xpath('./div[3]/abbr/text()').extract_first()
            comment_item['_id'] = comment_node.xpath('../@id').extract_first() + '_' + self.url[:100]
            yield comment_item

        next_page = self.host + response.xpath('//div[starts-with(@id,"see_next")]/a/@href').extract_first()
        if next_page:
            yield Request(url=next_page, callback=self.parse, dont_filter=True)
