import os
import pymongo
import requests
from hashlib import md5
from urllib.parse import urlencode
from multiprocessing import Pool


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}

def get_page_source(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception:
        print('error')


def get_content(json):
    if json['data']:
        for item in json['data']:
            title = item.get('title')
            image_urls = item.get('image_list')
            for image_url in image_urls:
                image = 'http://' + image_url.get('url').strip('//').replace('list', 'large')
                yield {
                    'image': image,
                    'title': title
                }


def save_to_file(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('已经下载过！')
    except requests.ConnectionError:
        print('连接失败!')


def save_to_mongo(data):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['jrtt']
    collection = db['jrtt_spider']
    if collection.insert(data):
        print('保存到MongoDB成功')


def main(page):
    params = {
        'offset': page,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3',
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    json = get_page_source(url)
    items = get_content(json)
    for item in items:
      # 保存至本地文件夹
        save_to_file(item)
      # 保存标题和链接到MongoDB数据库
      #   save_to_mongo(item)


if __name__ == '__main__':
    START = 1
    END = 20
    pool = Pool()
    groups = ([x * 20 for x in range(START, END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()