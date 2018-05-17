#!/usr/bin/env python
# encoding: utf-8
import json
import subprocess
import time
import web
import pymongo
import os

client = pymongo.MongoClient("localhost", 27017)
db = client['web']
collection = db['jobs']
urls = (
    '/', 'index',
    '/jobs', 'jobs',
    '/(tweets|person|relationship|comment)', 'tweets',
    '/static', 'static',
)

app = web.application(urls, globals())


class static:
    def GET(self):
        try:
            get_input = web.input(_method='get')
            file_path = os.getcwd() + '/../../spider/' + get_input['file']
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                return json.dumps({'code': 0, 'message': 'get file successfully', 'data': [text]})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class index:
    def GET(self):
        return 'Hello'


class jobs:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        try:
            get_input = web.input(_method='get')
            page = int(get_input['page'])
            limit = int(get_input['limit'])
            jobs = collection.find().limit(limit).skip(limit * (page - 1))
            data = [job for job in jobs]
            count = collection.find().count()
            return json.dumps({'code': 0, 'message': 'query job successfully', 'count': count, 'data': data})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})

    def POST(self):
        web.header("Access-Control-Allow-Origin", "*")
        post_input = web.input(_method='post')
        try:
            keyword = post_input['keyword']
            website = post_input['website']
            M = post_input['M']
            N = post_input['N']
            data = {'keyword': keyword, 'website': website, 'create_timestamp': int(time.time()),
                    }
            data['_id'] = data['create_timestamp']
            command = 'scrapy crawl search -a keyword={} -s LOG_FILE=log/{}_search.log -s DBNAME={} -s CNAME={}'.format(
                keyword,
                data['_id'],
                data['_id'],
                "search")
            p = subprocess.Popen([command], cwd=os.getcwd() + '/../../spider/{}'.format(website), shell=True)
            data['pid'] = p.pid
            data['status'] = 'running-search'
            data['M'] = M
            data['N'] = N
            data['log'] = '{}/log/{}_search.log'.format(website, data['_id'])
            data['db'] = '{}'.format(data['_id'])
            data['run_timestamp'] = int(time.time())
            collection.insert(data)
            return json.dumps({'code': 0, 'message': 'add job successfully', 'data': [data]})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


class tweets:
    def GET(self, collection_name):
        try:
            get_input = web.input(_method='get')
            page = int(get_input['page'])
            limit = int(get_input['limit'])
            job_id = get_input['job_id']
            temp_db = client['{}'.format(job_id)]
            if collection_name == 'tweets':
                type = get_input['type']
                temp_collection = temp_db['Tweets_{}'.format(type)]
            elif collection_name == 'person':
                temp_collection = temp_db['Information']
            elif collection_name == 'relationship':
                temp_collection = temp_db['Relationship']
            else:
                temp_collection = temp_db['Comment']
            count = temp_collection.find().count()
            datas = temp_collection.find().limit(limit).skip(limit * (page - 1))
            return_data = [data for data in datas]

            return json.dumps({'code': 0, 'message': 'query tweet successfully', 'count': count, 'data': return_data})
        except Exception as e:
            return json.dumps({'code': 1, 'message': str(e)})


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
