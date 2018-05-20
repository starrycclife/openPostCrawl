#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline
import sys

M = sys.argv[1]
N = sys.argv[2]
jobid = sys.argv[3]
command = 'scrapy crawl person -a M={} -a N={} -a job_id={} -s LOG_FILE=log/{}.log -s DBNAME={} -s CNAME={}'.format(
    M, N, jobid, jobid, jobid, 'person'
)
cmdline.execute(command.split(" "))
