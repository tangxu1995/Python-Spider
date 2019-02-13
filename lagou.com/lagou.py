import requests
import json
import pymongo
import pymysql


class lagouSpider():
    def __init__(self, page):
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
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
            'Cookie': 'JSESSIONID=ABAAABAAADEAAFI39E78145601C723EFA8A12C7BB285445; _ga=GA1.2.1028451105.1550040382; _gid=GA1.2.448435563.1550040382; user_trace_token=20190213144622-134f0285-2f5b-11e9-8188-5254005c3644; LGUID=20190213144622-134f0653-2f5b-11e9-8188-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; LG_LOGIN_USER_ID=8eac5f0f1324bf2dcaecb843477a4b2d030039875eedfb7f; _putrc=411996842906BB54; login=true; unick=%E5%94%90%E6%97%AD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=85f290ea41114cc3addbfc9a11238f284cf80e822b6429f2; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550040383,1550041495; hasDeliver=10; TG-TRACK-CODE=search_code; LGSID=20190213160334-dc7adf9c-2f65-11e9-818c-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26city%3D%25E5%258C%2597%25E4%25BA%25AC; X_MIDDLE_TOKEN=f6557e08b0ecf168a98c40d8a415fc52; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1550045097; LGRID=20190213160456-0d5dcbec-2f66-11e9-b6af-525400f775ce; SEARCH_ID=4877253727aa4197bc1ab82e29218289'
        }

        self.params = {
            'first': 'true',
            'pn': page,
            'kd': 'python'
        }
        self.client = pymongo.MongoClient('localhost', 27017)
        self.mongo_db = self.client['spiders']
        self.mysql_db = pymysql.connect('localhost', 'root', 'root', 'spiders')

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
            yield {
                '职位名称': position_name,
                '职位薪资': position_salary,
                '工作年份': position_workYear,
                '公司名称': company_name,
                '公司领域': company_type,
                '公司地址': company_addr,
                '公司规模': company_size
            }


    def save_to_txtfile(self, item):
        with open('position.json', 'a') as f:
            f.write(item)

    def save_to_mongodb(self, item):
        collection = self.mongo_db['lagou']
        collection.insert_one(item)

    def save_to_mysql(self, item):
        cursor = self.mysql_db.cursor()
        sql = '''
            INSERT INTO lagou(position_name, position_salary, position_workYear, company_name, company_type, 
            company_addr, company_size) VALUES (%s, %s, %s, %s, %s, %s, %s)     
        '''
        cursor.execute(sql, (item['职位名称'], item['职位薪资'], item['工作年份'], item['公司名称'], item['公司领域'],
                             item['公司地址'], item['公司规模']))
        self.mysql_db.commit()


    def start_spider(self):
        html = self.get_page_source(self.url)
        if 'false' in html:
            print('操作频繁，请稍后再试')
        else:
            positionInfos = self.get_job(html)
            for positionInfo in positionInfos:
                print(positionInfo)
                self.save_to_txtfile(str(positionInfo) + '\n')
                self.save_to_mongodb(positionInfo)
                self.save_to_mysql(positionInfo)
                self.mysql_db.close()


if __name__ == '__main__':
    for page in range(1, 10):
        lagou = lagouSpider(page)
        lagou.start_spider()
