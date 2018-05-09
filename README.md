# openPostCrawl

根据关键词对主流舆情网站进行数据抓取.

网站包括:weibo,facebook,twitter,YouTube

## 抓取要求

### weibo/facebook/twitter

1. 根据关键词抓取含有该关键词的微博数据

2. 根据上述微博筛选出一批种子用户

3. 抓取种子用户的微博数据/粉丝数据

4. 每个种子用户根据社交关系(粉丝)向外扩M层，得到的用户进行爬取（用户信息、社交关系、帖子内容）
  
### YouTube

1. 抓取指定用户上传的视频数据

## web界面

1. 提供关键词入口

2. 每个关键词爬虫状态(就绪/运行/结束)

3. 爬虫数据展示

4. 高级可视化，词云/数据统计等

## 贡献代码

1. 克隆代码:
`git clone git@github.com:nghuyong/openPostCrawl.git`
2. 在本地创建自己的分支:
`git branch mybranch`
3. 切换到自己的分支上:
`git checkout mybranch`
4. 开始开发，并及时commit
5. 准备提交代码上线时候，首先fetch最新的代码：
`git fetch origin/master`
6. 与本地的自己分支进行合并:
`git merge orgin/master`
7. 提交代码
`git push origin mybranch`
8. 在远端提交Pull request