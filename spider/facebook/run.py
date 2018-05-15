#!/usr/bin/env python
# encoding: utf-8
from scrapy import cmdline

# cmdline.execute("scrapy crawl search_post".split(" "))
# cmdline.execute("scrapy crawl person_post".split(" "))
# cmdline.execute("scrapy crawl person_info".split(" "))
# cmdline.execute("scrapy crawl post_comment".split(" "))
cmdline.execute("scrapy crawl person_friend".split(" "))
