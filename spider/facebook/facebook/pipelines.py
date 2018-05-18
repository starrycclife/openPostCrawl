# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from pymongo.errors import DuplicateKeyError

from facebook.items import PostItem, PersonItem, CommentItem, PersonFriendItem
from scrapy.conf import settings


class MongoDBPipeline(object):
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        # dbname = settings["MONGODB_DBNAME"]
        clinet = pymongo.MongoClient(host=host, port=port)
        db = clinet["{}".format(settings['DBNAME'])]
        self.Posts = db["Tweets_{}".format(settings['CNAME'])]
        self.Persons = db["Information"]
        self.Comments = db["Comments"]
        self.Friends = db["Relationships"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, PostItem):
            self.insert_item(self.Posts, item)
        if isinstance(item, PersonItem):
            self.insert_item(self.Persons, item)
        if isinstance(item, CommentItem):
            self.insert_item(self.Comments, item)
        if isinstance(item, PersonFriendItem):
            self.insert_item(self.Friends, item)
        return item

    def insert_item(self, collection, item):
        try:
            collection.insert(dict(filter(lambda x: x[1], dict(item).items())))
        except DuplicateKeyError:
            logging.warning('数据重复： %s', item['_id'])
            pass
