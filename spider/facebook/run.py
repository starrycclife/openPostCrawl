#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline

# cmdline.execute("scrapy crawl search -a keyword=营养早餐 -s DBNAME=Facebook -s CNAME=search".split(" "))
cmdline.execute("scrapy crawl person -a M=1 -a N=100 -s DBNAME=Facebook -s CNAME=person".split(" "))
