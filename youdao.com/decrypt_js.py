import hashlib
import random
import time
import requests
from urllib.parse import urlencode


class YoudaoFanyi(object):

    def __init__(self, key):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=true'
        self.key = key

    def getSalt(self):
        """
        获取 salt 参数
        :return: salt 参数
        """
        salt = int(time.time() * 1000) + random.randint(0, 10)

        return salt

    def getMD5(self, v):
        """
        加密值
        :param v: 将加密的值
        :return: 加密后的值
        """
        md5 = hashlib.md5()

        md5.update(v.encode('utf-8'))

        sign = md5.hexdigest()

        return sign

    def getSign(self, salt):
        """
        获取 sign 参数
        :param salt: salt
        :return: sign 参数
        """
        sign = "fanyideskweb" + self.key + str(salt) + 'p09@Bn{h02_BIEe]$P^nG'

        sign = self.getMD5(sign)

        return sign

    def getbv(self):
        """
        获取 bv 参数
        :return: bv 参数
        """
        appVersion = '5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'

        md5 = hashlib.md5()

        md5.update(appVersion.encode('utf-8'))

        bv = md5.hexdigest()

        return bv

    def getts(self):
        """
        获取 ts 参数
        :return: ts 参数
        """
        ts = int(time.time() * 1000)

        return ts

    def main(self):

        salt = self.getSalt()

        data = {
            'i': self.key,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': str(salt),
            'sign': self.getSign(salt),
            'ts': self.getts(),
            'bv': self.getbv(),
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false'
        }

        data = urlencode(data).encode()

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Length": str(len(data)),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "ANTICSRF=cleared; P_INFO=xiezhengwei2008; NTES_OSESS=cleared; S_OINFO=; OUTFOX_SEARCH_USER_ID=1515915441@10.168.8.61; JSESSIONID=aaaAAT3WmCOQ6-0Zne_Hw; OUTFOX_SEARCH_USER_ID_NCOO=1910496961.1878116; ___rl__test__cookies=1548303281445",
            "Host": "fanyi.youdao.com",
            "Origin": "http://fanyi.youdao.com",
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }

        response = requests.post(self.url, data=data, headers=headers)

        if response.status_code == 200:

            result = response.json().get('translateResult')[0][0].get('tgt')

            print('Translation result: %s' % result)


if __name__ == '__main__':
    while True:
        word = input("Please enter the word you want to translate:")
        if word == 'quit':
            break
        youdao = YoudaoFanyi(word)
        youdao.main()
