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
)

app = web.application(urls, globals())


class index:
    def GET(self):
        return 'Hello'


class jobs:
    def GET(self):
        try:
            get_input = web.input(_method='get')
            page = int(get_input['page'])
            limit = int(get_input['limit'])
            jobs = collection.find().limit(limit).skip(limit * (page - 1))
            data = [job for job in jobs]
            return json.dumps({'code': 1, 'message': 'query job successfully', 'count': len(data), 'data': data})
        except Exception as e:
            return json.dumps({'code': 0, 'message': str(e)})

    def POST(self):
        post_input = web.input(_method='post')
        try:
            keyword = post_input['keyword']
            website = post_input['website']
            M = post_input['M']
            N = post_input['N']
            data = {'keyword': keyword, 'website': website, 'create_timestamp': int(time.time()),
                    }
            data['_id'] = data['create_timestamp']
            command = 'scrapy crawl search -a keyword={} -s LOG_FILE=log/{}.log -s DBNAME={}'.format(keyword,
                                                                                                     data['_id'],
                                                                                                     data['_id'])
            p = subprocess.Popen([command], cwd=os.getcwd() + '/../../spider/{}'.format(website), shell=True)
            data['pid'] = p.pid
            data['status'] = 'running'
            data['M'] = M
            data['N'] = N
            data['log'] = '{}/log/{}.log'.format(website, data['_id'])
            data['db'] = '{}_{}'.format(website, data['_id'])
            data['run_timestamp'] = int(time.time())
            collection.insert(data)
            return json.dumps({'code': 1, 'message': 'add job successfully', 'data': [data]})
        except Exception as e:
            return json.dumps({'code': 0, 'message': str(e)})


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
