#!/usr/bin/env python
# encoding: utf-8
import json
import subprocess
import time
import web
import pymongo
import os
import shutil

from pymongo.errors import DuplicateKeyError

client = pymongo.MongoClient("localhost", 27017)
db = client['web']
collection = db['jobs']
urls = (
    '/api/jobs', 'jobs',
    '/api/(tweet-search|tweet-person|person|relationship|comment)', 'tweets',
    '/api/static', 'static',
    '/api/youtube-videos', 'videos',
    '/api/cookies', 'cookies',
)

app = web.application(urls, globals())


class cookies:
    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='post')
            website = get_input['website']
            cookie = get_input['cookie']
            cookie_collection = db['cookies']
            try:
                cookie_collection.insert({'_id': website, 'cookie': cookie})
            except DuplicateKeyError:
                cookie_collection.find_one_and_update({'_id': website}, {'$set': {'cookie': cookie}})
            return json.dumps({'code': 0, 'message': 'set cookie successfully', 'data': []})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class videos:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            job_id = get_input['job_id']
            videos = os.listdir('static/youtube_videos/{}'.format(job_id))
            return json.dumps({'code': 0, 'message': 'get videos successfully', 'data': [videos]})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class static:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            file_path = os.getcwd() + '/../../spider/' + get_input['file']
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                return json.dumps({'code': 0, 'message': 'get file successfully', 'data': [text]})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class jobs:
    def OPTIONS(self):
        web.header("Access-Control-Allow-Origin", "*")
        web.header("Access-Control-Allow-Methods", "*")
        return None

    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            page = int(get_input['page'])
            limit = int(get_input['limit'])
            website = get_input['website']
            if website == 'youtube':
                jobs = collection.find({'website': 'youtube'}).sort("_id", pymongo.DESCENDING).limit(limit).skip(
                    limit * (page - 1))
                count = collection.find({'website': 'youtube'}).count()
            else:
                jobs = collection.find({'website': {'$ne': 'youtube'}}).sort("_id", pymongo.DESCENDING).limit(
                    limit).skip(limit * (page - 1))
                count = collection.find({'website': {'$ne': 'youtube'}}).count()
            data = [job for job in jobs]

            return json.dumps({'code': 0, 'message': 'query job successfully', 'count': count, 'data': data})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    def DELETE(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            job_id = get_input['job_id']
            job = collection.find_one({'_id': int(job_id)})
            """
            1.先杀死进程
            """
            os.system('kill -9 {}'.format(job['pid']))
            """
            2.删除数据库
            """
            if job['website'] == 'youtube':
                shutil.rmtree(os.getcwd() + '/' + job['video'])
            else:
                client.drop_database(job['db'])
            """
            3.删除日志
            """
            os.remove(os.getcwd() + '/../../spider/' + job['log'])
            collection.remove(int(job_id))
            return json.dumps({'code': 0, 'message': 'delete job successfully'})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        post_input = web.input(_method='post')
        data = {}
        data['create_timestamp'] = int(time.time())
        data['_id'] = data['create_timestamp']
        data['run_timestamp'] = int(time.time())
        try:
            website = post_input['website']
            data['website'] = website
            if website == 'weibo' or website == 'twitter' or website == 'facebook':
                keyword = post_input['keyword']
                M = post_input['M']
                N = post_input['N']
                data['keyword'] = keyword
                if website == 'weibo' or website == 'facebook':
                    command = 'scrapy crawl search -a keyword={} -s LOG_FILE=log/{}.log -s DBNAME={} -s CNAME={}'.format(
                        keyword,
                        data['_id'],
                        data['_id'],
                        "search")
                    data['log'] = '{}/log/{}.log'.format(website, data['_id'])
                else:
                    command = "python run.py {} {} {} {}".format(keyword, N, M, data['_id'])
                    data['log'] = '{}/log/{}.log'.format(website, data['_id'])
                data['M'] = M
                data['N'] = N
                data['db'] = '{}'.format(data['_id'])
                data['status'] = 'running-search'
            else:
                index_url = post_input['index_url']
                """
                https://www.youtube.com/watch?v=BaW_jenozKc
                """
                command = "python run.py {} {}".format(data['_id'], index_url)
                data['status'] = 'running'
                data['log'] = '{}/log/{}.log'.format(website, data['_id'])
                data['video'] = '{}/video/{}'.format(website, data['_id'])
            p = subprocess.Popen([command], cwd=os.getcwd() + '/../../spider/{}'.format(website), shell=True)
            data['pid'] = p.pid
            collection.insert(data)
            return json.dumps({'code': 0, 'message': 'add job successfully', 'data': [data]})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class tweets:
    def GET(self, collection_name):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            page = int(get_input['page'])
            limit = int(get_input['limit'])
            job_id = get_input['job_id']
            temp_db = client['{}'.format(job_id)]
            if collection_name == 'tweet-search':
                temp_collection = temp_db['Tweets_search'.format(type)]
            elif collection_name == "tweet-person":
                temp_collection = temp_db['Tweets_person'.format(type)]
            elif collection_name == 'person':
                temp_collection = temp_db['Information']
            elif collection_name == 'relationship':
                temp_collection = temp_db['Relationships']
            else:
                temp_collection = temp_db['Comments']
            count = temp_collection.find().count()
            datas = temp_collection.find().limit(limit).skip(limit * (page - 1))
            return_data = [data for data in datas]
            return json.dumps({'code': 0, 'message': 'query tweet successfully', 'count': count, 'data': return_data})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
