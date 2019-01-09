import requests
import json
import time
import pymongo


class videoInfo_Spider(object):
    def __init__(self, aid):
        self.video_url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={}'.format(aid)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
        }

    def get_source(self, url):
        time.sleep(0.4)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print('访问出错')

    def parse(self, items):
        if items.get('data'):
            info = items.get('data')
            id = info.get('aid')
            view = info.get('view')
            danmaku = info.get('danmaku')
            reply = info.get('reply')
            favorite = info.get('favorite')
            coin = info.get('coin')
            share = info.get('share')
            yield {
                'id': id,
                '观看数': view,
                '弹幕数': danmaku,
                '喜欢数': favorite,
                '回复数': reply,
                '硬币数': coin,
                '分享数': share
            }

    def save_to_mongo(self, item):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['BILIBILI']
        collection = db['videoInfo']
        if collection.insert(item):
            print('保存到MongoDB成功')

    def run(self):
        html = self.get_source(self.video_url)
        items = self.parse(html)
        for item in items:
            print(item)
            self.save_to_mongo(item)


if __name__ == '__main__':

    time1 = time.time()
    for aid in range(1, 40000890):
        spider = videoInfo_Spider(aid)
        spider.run()
    time2 = time.time()
    print('cost time: %s' % (time2-time1))