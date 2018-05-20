#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline

# cmdline.execute("scrapy crawl search -a keyword=营养早餐 -s DBNAME=Facebook -s CNAME=search".split(" "))
# cmdline.execute("scrapy crawl person -a M=1 -a N=100 -s DBNAME=Facebook -s CNAME=person".split(" "))
import sys

M = sys.argv[1]
N = sys.argv[2]
jobid = sys.argv[3]
command = 'scrapy crawl person -a M={} -a N={} -s LOG_FILE=log/{}.log -s DBNAME={} -s CNAME={}'.format(
    M, N, jobid, jobid, 'person'
)
cmdline.execute(command.split(" "))
