#!/usr/bin/env python
# encoding: utf-8
import pymongo
import time
import youtube_dl
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # logger的总开关，只有大于Debug的日志才能被logger对象处理
# 第二步，创建一个handler，用于写入日志文件

if __name__ == "__main__":
    job_id = sys.argv[1]
    index_url = sys.argv[2]
    logger.info(index_url)
    # job_id = '123456789'
    file_handler = logging.FileHandler('log/{}.log'.format(job_id), mode='at', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 创建该handler的formatter
    file_handler.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    )
    # 添加handler到logger中
    logger.addHandler(file_handler)
    ydl_opts = {
        'logger': logger,
        'ignoreerrors': True,
        'outtmpl': '../../web/server/static/youtube_videos/{}/%(title)s.%(ext)s'.format(job_id)
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([index_url])
    except Exception as e:
        logger.info(str(e))
    client = pymongo.MongoClient("localhost", 27017)
    db = client['web']
    collection = db['jobs']
    job = collection.find_one({'_id': int(job_id)})
    job['status'] = 'finish'
    job['finish_timestamp'] = int(time.time())
    collection.save(job)
