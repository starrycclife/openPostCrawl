# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    NickName = Field()  # 昵称
    Gender = Field()  # 性别
    Province = Field()  # 所在省
    City = Field()  # 所在城市
    BriefIntroduction = Field()  # 简介
    Birthday = Field()  # 生日
    Num_Tweets = Field()  # 微博数
    Num_Follows = Field()  # 关注数
    Num_Fans = Field()  # 粉丝数
    SexOrientation = Field()  # 性取向
    Sentiment = Field()  # 感情状况
    VIPlevel = Field()  # 会员等级
    Authentication = Field()  # 认证
    URL = Field()  # 首页链接


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()
    name_1 = Field()
    user_id_1 = Field()
    created_at_1 = Field()
    content_1 = Field()
    weibo_url_1 = Field()
    is_repost = Field()
    like_num = Field()
    repost_num = Field()
    comment_num = Field()
    name_2 = Field()
    user_id_2 = Field()
    created_at_2 = Field()
    content_2 = Field()
    weibo_url_2 = Field()


class RelationshipsItem(Item):
    """ 用户关系，只保留与关注的关系 """
    fan_id = Field()
    followed_id = Field()  # 被关注者的ID
    _id = Field()


class CommentItem(Item):
    """
    微博评论
    """
    weibo_url = Field()
    comment_user = Field()
    _id = Field()
    content = Field()
    created_at = Field()
