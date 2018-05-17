#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline

cmdline.execute("scrapy crawl person -a keyword=营养 -s DBNAME=1234567".split(" "))