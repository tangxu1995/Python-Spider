import requests
import json
import time
import pymongo
# from multiprocessing import Process, Queue
from threading import Thread
from queue import Queue


class videoInfo_Spider(Thread):
    def __init__(self, url, q):
        super(videoInfo_Spider, self).__init__()
        self.video_url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
        }
        self.q = q
        # self.pool = multiprocessing.Pool()

    def get_source(self, url):
        time.sleep(0.4)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('访问出错')

    def parse(self):
        items = self.get_source(self.video_url)
        if items.get('data'):
            info = items.get('data')
            id = info.get('aid')
            view = info.get('view')
            danmaku = info.get('danmaku')
            reply = info.get('reply')
            favorite = info.get('favorite')
            coin = info.get('coin')
            share = info.get('share')
            self.q.put(id + view)
            # yield {
            #     'id': id,
            #     '观看数': view,
            #     '弹幕数': danmaku,
            #     '喜欢数': favorite,
            #     '回复数': reply,
            #     '硬币数': coin,
            #     '分享数': share
            # }

    def save_to_mongo(self, item):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['BILIBILI']
        collection = db['videoInfo']
        if collection.insert(item):
            print('保存到MongoDB成功')

    def run(self):
        # html = self.get_source(self.video_url)
        # items = self.parse(html)
        # for item in items:
        #     print(item)
        #     self.save_to_mongo(item)
        self.parse()

def main():

    # 创建队列
    q = Queue()

    # 构造所有url
    base_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'
    url_list = [base_url.format(aid) for aid in range(1, 1000)]

    # 保存线程
    Thread_list = []

    # 创建并启动线程
    for url in url_list:
        p = videoInfo_Spider(url, q)
        p.start()
        Thread_list.append(p)

    #
    for i in Thread_list:
        i.join()

    while not q.empty():
        print(q.get())


if __name__ == '__main__':
    start = time.time()
    main()
    print('cost time:%s' % (time.time() - start))