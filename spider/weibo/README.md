# 微博爬虫

基于scrapy框架实现

## 运行

### weibo_search_spider
根据关键词抓取时间、地点的微博语料，采用微博搜索接口.

在本目录下，`scrapy crawl search` 运行

### weibo_person_spider
指定种子用户，并根据粉丝关系向外扩3层，对得到的用户进行爬取

每个用户抓取内容包括，个人信息，全部的微博，粉丝列表，关注列表

在本目录下，`scrapy crawl person` 运行