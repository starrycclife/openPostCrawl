# Facebook爬虫

基于scrapy框架实现

每次请求延迟10秒，防止被限速

## 运行

### search_spider
根据关键词抓取时间、地点的帖子语料，采用移动端Facebook搜索接口.

在本目录下，`scrapy crawl search` 运行

### person_info
抓取个人信息

在本目录下，`scrapy crawl person_info` 运行