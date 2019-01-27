import json
import re
import os
import requests
from lxml import etree
from urllib.request import urlretrieve

base_url = 'https://pvp.qq.com/web201605/herodetail/{}.shtml'
json_file = 'https://pvp.qq.com/web201605/js/herolist.json'
response = requests.get(json_file)

hero_json = json.loads(response.text)
hero_id_list = []

for hero in hero_json:
    hero_id = hero.get('ename')
    hero_name = hero.get('cname')
    hero_id_list.append(hero_id)
    os.mkdir('./' + hero_name)

hero_detail_page = [base_url.format(hero_id) for hero_id in hero_id_list]
pf_base_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'

for hero_page in hero_detail_page:
    items = hero_page.split("/")[5]
    item = re.findall('\d+', items)[0]
    response = requests.get(hero_page)
    tree = etree.HTML(response.content)
    hero_name = tree.xpath("//div[@class='cover']/h2/text()")[0]
    pf_name = tree.xpath("//div[@class='pic-pf']/ul[1]/@data-imgname")[0]
    pfs = pf_name.split("|")

    for num in range(1, len(pfs) + 1):
        pf_url = pf_base_url.format(item, item, num)
        file_path = './' + hero_name + '/' + pfs[num-1] + '.jpg'
        if not os.path.exists(file_path):
            urlretrieve(pf_url, file_path)
            print(hero_name + '-' + pfs[num-1] + '-->' + pf_url)




