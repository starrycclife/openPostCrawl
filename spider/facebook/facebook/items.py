# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PostItem(scrapy.Item):
    """ 贴文 """
    _id = Field()
    avatar_url = Field()
    user_url = Field()
    user_name = Field()
    post = Field()
    video_urls = Field()
    img_urls = Field()
    date_time = Field()
    like_num = Field()
    comments_num = Field()
    url = Field()


class PersonItem(scrapy.Item):
    """ 用户信息 """
    _id = Field()
    name = Field()
    job_name = Field()
    job_time = Field()
    school_name = Field()
    school_subject = Field()
    school_time = Field()
    location = Field()
    hometown = Field()
    contact = Field()
    sex = Field()
    birthday = Field()
    relationship = Field()


class CommentItem(scrapy.Item):
    """ 评论 """
    _id = Field()
    content = Field()
    username = Field()
    user_url = Field()
    datetime = Field()


class PersonFriendItem(scrapy.Item):
    """ 好友关系 """
    _id = Field()
    user_url = Field()
    friend_name = Field()
    friend_url = Field()
