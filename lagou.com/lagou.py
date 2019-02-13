import requests
from lxml import etree
import json
from urllib.parse import urlencode


class lagouSpider():
    def __init__(self, page):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&district=%E6%9C%9D%E9%98%B3%E5%8C%BA&needAddtionalResult=false'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '25',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&city=%E5%8C%97%E4%BA%AC&district=%E6%9C%9D%E9%98%B3%E5%8C%BA',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'JSESSIONID=ABAAABAAADEAAFI39E78145601C723EFA8A12C7BB285445; _ga=GA1.2.1028451105.1550040382; _gid=GA1.2.448435563.1550040382; user_trace_token=20190213144622-134f0285-2f5b-11e9-8188-5254005c3644; LGSID=20190213144622-134f0431-2f5b-11e9-8188-5254005c3644; LGUID=20190213144622-134f0653-2f5b-11e9-8188-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; LG_LOGIN_USER_ID=8eac5f0f1324bf2dcaecb843477a4b2d030039875eedfb7f; _putrc=411996842906BB54; login=true; unick=%E5%94%90%E6%97%AD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=85f290ea41114cc3addbfc9a11238f284cf80e822b6429f2; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550040383,1550041495; hasDeliver=10; _gat=1; TG-TRACK-CODE=index_search; SEARCH_ID=f7c9daf0212b4c47957b83de7ec2e81a; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550042225; LGRID=20190213151704-5d800bde-2f5f-11e9-818a-5254005c3644'
        }

        self.params = {
            'first': 'false',
            'pn': page,
            'kd': 'python'
        }

    def get_page_source(self, url):
        r = requests.post(url, data=self.params, headers=self.headers)
        if r.status_code == 200:
            return r.text
        else:
            return None

    def get_job(self, html):
        data = json.loads(html)
        jobs = data['content']['positionResult']['result']
        for job in jobs:
            position_name = job['positionName']
            position_salary = job['salary']
            position_workYear = job['workYear']
            company_name = job['companyShortName']
            company_type = job['industryField']
            company_addr = job['district']
            company_size = job['companySize']

            print(position_name, position_salary, position_workYear,
                  company_name, company_type, company_addr, company_size)

    def start_spider(self):
        html = self.get_page_source(self.url)
        self.get_job(html)


if __name__ == '__main__':
    for page in range(1, 10):
        lagou = lagouSpider(page)
        lagou.start_spider()
