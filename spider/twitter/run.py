#!/usr/bin/env python
# encoding: utf-8
from pprint import pprint

import tweepy

from settings import ConsumerKey, ConsumerSecret, AccessToken, AccessTokenSecret


class Twitter:
    def __init__(self):
        auth = tweepy.OAuthHandler(ConsumerKey, ConsumerSecret)
        auth.set_access_token(AccessToken, AccessTokenSecret)
        self.api = tweepy.API(auth)

    def search_tweet(self, keyword):
        """
        根据关键词，抓取twitter
        """
        search_results = self.api.search(q=keyword, count=100)
        for tweet in search_results:
            if 'text' in tweet._json:
                print(tweet._json['text'])

    def get_friend(self, user_id):
        """
        根据用户id，获取好友
        """
        friends = self.api.friends(user_id=user_id)

    def get_user_timeline(self,user_id):
        """
        根据用户id，获取twitter
        """
        results = self.api.user_timeline(user_id=user_id)
        for tweet in results:
            pprint(tweet._json)

    def get_tweet_reply(self,twitter_id):
        """
        根据twitter id，和这个Twitter的用户名，获取回复
        """
        tweet = self.api.get_status(id='996401064155873286')
        tweets = self.api.search(q='@CGTNOfficial')
        for tweet in tweets:
            if tweet.in_reply_to_status_id == 996401064155873286:
                pprint(tweet._json)
