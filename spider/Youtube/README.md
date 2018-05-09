# Youtube爬虫

抓取指定用户上传的视频

安装并采用[youtube-dl](https://github.com/rg3/youtube-dl)工具下载

比如下载用户VOAchina的全部视频**需要代理**

```bash
youtube-dl -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/user/VOAchina/videos
```
