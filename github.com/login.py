import requests
from lxml import etree


class github_login(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36',
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def get_token(self):
        html = self.session.get(self.login_url, headers=self.headers)
        response = etree.HTML(html.text)
        token = response.xpath("//input[@name='authenticity_token']/@value")[0]
        return token

    def parse(self, html):
        response = etree.HTML(html)
        name = response.xpath("//dl[@class='form-group'][1]/dd[1]/input/@value")[0]
        location = response.xpath("//dl[@class='form-group'][6]/dd[1]/input/@value")[0]
        print('姓名: %s, 地址: %s' % (name, location))

    def login(self, token, email, password):

        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': token,
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=data, headers=self.headers)
        if response.status_code == 200:
            print('登录成功，正在跳转到个人信息...')

        response = self.session.get(self.logined_url, headers=self.headers)
        self.parse(response.text)


if __name__ == '__main__':
    login = github_login()
    token = login.get_token()
    login.login(token, 'username', 'password')