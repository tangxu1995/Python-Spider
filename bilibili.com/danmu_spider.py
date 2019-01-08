import requests
from lxml import etree


class Danmu_Spider(object):
    def __init__(self):
        self.danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=57763167'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
        }

    def get_file(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            with open('danmu.xml', 'wb') as f:
                f.write(response.content)
        else:
            print('访问出错')

    def parse_danmus(self, file):
        selector = etree.parse(file, etree.HTMLParser())
        items = selector.xpath("//d//text()")
        items = set(items)
        return items

    def run(self):
        self.get_file(self.danmu_url)
        danmus = self.parse_danmus('danmu.xml')
        print('弹幕数量: %s'% len(danmus))
        print(danmus)


if __name__ == "__main__":
    spider = Danmu_Spider()
    spider.run()