#!/usr/bin/env python
# encoding: utf-8
from pprint import pprint

import os
import pymongo
import time
import tweepy
from pymongo.errors import DuplicateKeyError

from settings import ConsumerKey, ConsumerSecret, AccessToken, AccessTokenSecret
import logging


class Twitter:
    def __init__(self, keyword, N, M, job_id):
        auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
        auth.set_access_token(AccessToken, AccessTokenSecret)
        self.api = tweepy.API(auth)
        self.keyword = keyword
        self.M = int(M)
        self.N = int(N)
        self.job_id = int(job_id)
        self.client = pymongo.MongoClient("localhost", 27017)
        self.db = self.client['{}'.format(self.job_id)]

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理

        # 第二步，创建一个handler，用于写入日志文件  
        file_handler = logging.FileHandler('log/{}.log'.format(job_id), mode='at', encoding='utf-8')
        file_handler.setLevel(logging.INFO)  # 输出到file的log等级的开关
        # 创建该handler的formatter
        file_handler.setFormatter(
            logging.Formatter(
                fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        )
        # 添加handler到logger中
        self.logger.addHandler(file_handler)
        self.job = self.client['web']['jobs'].find_one({"_id": self.job_id})

    def insert(self, collection, data):
        try:
            collection.insert(data)
        except DuplicateKeyError:
            pass

    def search(self):
        """
        根据关键词，抓取twitter
        """
        self.logger.info('start search keyword {}'.format(self.keyword))
        search_results = self.api.search(q=self.keyword, count=100)
        collection = self.db['Tweets_search']
        for tweet in search_results:
            data = {}
            data['created_at'] = tweet._json['created_at']
            data['_id'] = tweet._json['id_str']
            data['retweet_count'] = tweet._json['retweet_count']
            data['content'] = tweet._json['text']
            data['user'] = tweet._json['user']['id_str']
            self.logger.info('insert new search tweet {}'.format(data['_id']))
            self.insert(collection, data)
        self.logger.info('finish search keyword')
        self.job['status'] = 'running-person'
        self.client['web']['jobs'].save(self.job)
        self.person()

    def person(self):
        collection = self.db['Tweets_search']
        tweets = collection.find().limit(self.N)
        for tweet in tweets:
            self.information(tweet['user'], 0)
            time.sleep(3)
        self.job['status'] = 'finish'
        self.job['finish_timestamp'] = int(time.time())
        self.client['web']['jobs'].save(self.job)

    def information(self, user_id, level):
        user = self.api.get_user(user_id=user_id)
        collection = self.db['Information']
        data = {}
        data['_id'] = user._json['id_str']
        data['description'] = user._json['description']
        data['followers_count'] = user._json['followers_count']
        data['friends_count'] = user._json['friends_count']
        data['name'] = user._json['name']
        self.logger.info('insert new information {}'.format(data['_id']))
        self.insert(collection, data)
        time.sleep(3)
        self.get_user_timeline(user_id)
        time.sleep(3)
        if level < self.M:
            self.get_friend(user_id, level + 1)

    def get_friend(self, user_id, level):
        """
        根据用户id，获取好友
        """
        try:
            collection = self.db['Relationships']
            friends = self.api.friends(user_id=user_id)
            for friend in friends:
                data = {}
                data['_id'] = friend._json['id_str'] + '-' + user_id
                data['source'] = user_id
                data['friend'] = friend._json['id_str']
                self.logger.info('insert friend {}'.format(data['_id']))
                self.insert(collection, data)
                self.information(friend._json['id_str'], level)
        except Exception as e:
            logging.error(e)

    def get_user_timeline(self, user_id):
        """
        根据用户id，获取twitter
        """
        results = self.api.user_timeline(user_id=user_id, count=10)
        collection = self.db['Tweets_person']
        for tweet in results:
            data = {}
            data['created_at'] = tweet._json['created_at']
            data['_id'] = tweet._json['id_str']
            data['retweet_count'] = tweet._json['retweet_count']
            data['content'] = tweet._json['text']
            data['user'] = tweet._json['user']['id_str']
            self.logger.info('insert new person tweet {}'.format(data['_id']))
            self.insert(collection, data)


if __name__ == "__main__":
    import sys

    keyword = sys.argv[1]
    N = sys.argv[2]
    M = sys.argv[3]
    job_id = sys.argv[4]
    twitter = Twitter(keyword, N, M, job_id)
    twitter.search()
