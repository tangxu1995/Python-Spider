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
            'Cookie': 'user_trace_token=20181118002836-d55c7fff-ea85-11e8-a4f0-525400f775ce; LGUID=20181118002836-d55c8300-ea85-11e8-a4f0-525400f775ce; _ga=GA1.2.1412687184.1542636851; JSESSIONID=ABAAABAAAGGABCB85A160586B658EB4FFB432825E6D3960; LG_LOGIN_USER_ID=d432d55bcc9f26ff031dd3346b005e8c1c5812912f4180e0; _putrc=411996842906BB54; login=true; unick=%E5%94%90%E6%97%AD; TG-TRACK-CODE=index_resume; _gat=1; LGSID=20190220020618-0e2d5bee-3471-11e9-827b-5254005c3644; PRE_UTM=; PRE_HOST=www.baidu.com; PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D33r_f-2Pn0pAQtEHEmVDIn4NgUXPfggvCEw7sXf8_5y%26wd%3D%26eqid%3D9f38c4220000562b000000035c6c4595; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20190220020618-0e2d5dc2-3471-11e9-827b-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC'
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
