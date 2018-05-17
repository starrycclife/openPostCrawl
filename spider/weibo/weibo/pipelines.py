# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError
from scrapy.conf import settings
from weibo.items import RelationshipsItem, TweetsItem, InformationItem, RelationshipsItem, CommentItem


class MongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["weibo_{}".format(settings['DBNAME'])]
        self.Tweets = db["Tweets_{}".format(settings['CNAME'])]
        self.Information = db["Information"]
        self.Relationships = db["Relationships"]
        self.Comment = db["Comments"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TweetsItem):
            self.insert_item(self.Tweets, item)
        elif isinstance(item, InformationItem):
            self.insert_item(self.Information, item)
        elif isinstance(item, RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, CommentItem):
            self.insert_item(self.Comment, item)
        return item

    def insert_item(self, collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass
