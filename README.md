# openPostCrawl[演示视频](http://www.iqiyi.com/w_19rzd36265.html)

根据关键词对主流舆情网站进行数据抓取.

网站包括:weibo,facebook,twitter,YouTube

在线体验：http://159.89.53.122:8080/static/client/

## 抓取要求

### [weibo](https://github.com/nghuyong/openPostCrawl/tree/master/spider/weibo)/facebook/twitter

1. 根据关键词抓取含有该关键词的微博数据

2. 根据上述微博筛选出一批种子用户

3. 抓取种子用户的微博数据/粉丝数据

4. 每个种子用户根据社交关系(粉丝)向外扩M层，得到的用户进行爬取（用户信息、社交关系、帖子内容）
  
### [YouTube](https://github.com/nghuyong/openPostCrawl/tree/master/spider/Youtube)

1. 抓取指定用户上传的视频数据

## web界面

1. 提供关键词入口

2. 每个关键词爬虫状态(就绪/运行/结束)

3. 爬虫数据展示

4. 高级可视化，词云/数据统计等

## 贡献代码

1. 克隆代码:
`git clone https://github.com/nghuyong/openPostCrawl.git`
2. 开始开发，并及时commit
3. 准备提交代码上线时候，首先fetch最新的代码：
`git fetch origin/master`
4. 与本地的自己分支进行合并:
`git merge orgin/master`
5. 提交代码
`git push origin mybranch`
6. 在远端提交Pull request

## 运行
1.克隆代码:`git clone https://github.com/nghuyong/openPostCrawl.git && cd openPostCrawl`

2.创建虚拟环境: `virtualenv env --python=python3`

3.激活虚拟环境: `source env/bin/activate`

4.安装依赖: `pip install -r spider/requirements.txt`

5.执行配置脚本: `sh config.sh`

6.启动服务:`cd web/server && python webAPI.py`

7.打开:`{服务器IP地址}:8080/static/client`即可，

8.在抓取之前需要先手动填入weibo.cn和m.facebook.com的cookie

weibo.cn cookie示例:`OUTFOX_SEARCH_USER_ID_NCOO=1780588551.4011402; browser=d2VpYm9mYXhpYW4%3D; _T_WM=767a89eeec1856d21bf83f366492de34; H5_INDEX_TITLE=nghuyong; H5_INDEX=1; WEIBOCN_WM=9021_90008; ALF=1529416854; SCF=AsJyCasIxgS59OhHHUWjr9OAw83N3BrFKTpCLz2myUf2UW1ruMhAmBTi23s2T-eQTsPoicxMXQz2m484k6w1aCQ.; SUB=_2A252BfYdDeRhGeNN61EW-SbMwzmIHXVVCZpVrDV6PUJbktAKLUH5kW1NScpOi1XTkSJ-QbdpFhslP-HVyVojkIDu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfexCAdmDP14J1IQ4VfRHl5JpX5K-hUgL.Fo-0eheN1Kn71h-2dJLoIEqLxK-L12BL1heLxK-L12qLBoq_TCH8SbHWxFHWeEH8SCHFxb-4S7tt; SUHB=0QS5gRIlX5yNKX; SSOLoginState=1526826573; MLOGIN=1`
m.facebook.com 示例:`c_user=100026187121261; xs=19%3ABn7NOVf4AeVnng%3A2%3A1526379440%3A-1%3A-1;`
