#!/usr/bin/env python
# encoding: utf-8
import json

import time

import web

web.config.debug = True
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
        get_input = web.input(_method='get')
        print(get_input['keyword'])

    def POST(self):
        post_input = web.input(_method='post')
        print(post_input['keyword'])


application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
