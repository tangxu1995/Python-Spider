import requests
import re
import math
from lxml import etree


class dianping_spider():

    def __init__(self):
        self.start_url = 'https://www.dianping.com/suzhou/ch10/g110'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
            }

    def request_html(self, url):
        response = requests.get(url, headers=self.headers)
        try:
            if response.status_code == 200:
                return response.text
            elif "验证中心" in response.text:
                print('此 ip 被封！')
        except Exception as e:
            print(e.args)

    def get_number_css(self, html):
        number_css_url = re.compile('<link rel="stylesheet" type="text/css" href="//(s3plus.meituan.net.*?\.css)') \
                         .findall(html)[0]
        number_css_url = 'https://' + number_css_url
        return number_css_url

    def get_num_svg(self, css, svg_reg='nlo'):
        number_svg_url = re.compile('span\[class\^="%s"\].*?background\-image: url\((.*?)\);' % svg_reg).findall(css)[0]
        number_svg_url = 'https:' + number_svg_url
        return number_svg_url

    def analysis_svg_file(self, svg_url):
        response = requests.get(svg_url, headers=self.headers).content
        tree = etree.HTML(response)
        datas = tree.xpath("//text")
        last = 0
        index_and_num_list = {}
        for index, data in enumerate(datas):
            y_location = int(data.xpath("./@y")[0])
            num_list = data.xpath(".//text()")[0]
            index_and_num_list[num_list] = range(last, y_location + 1)
            last = y_location
        return index_and_num_list

    def get_css_and_px_dict(css_url, css_content, svg_reg='nlo'):
        find_datas = re.findall(r'(\.%s[a-zA-Z0-9-]+)\{background:(\-\d+\.\d+)px (\-\d+\.\d+)px' % svg_reg, css_content)
        css_name_and_px = {}
        for data in find_datas:
            # 属性对应的值
            span_class_attr_name = data[0][1:]
            # 偏移量
            offset = data[1]
            # 阈值
            position = data[2]
            css_name_and_px[span_class_attr_name] = [offset, position]
        return css_name_and_px

    def analysis_main_page(self, html, css_and_px_dict, svg_threshold_and_int_dict):
        tree = etree.HTML(html)
        shops = tree.xpath('//div[@id="shop-all-list"]/ul/li')
        for shop in shops:

            comments_num = 0
            name = shop.xpath('.//div[@class="tit"]/a')[0].attrib["title"]
            attr_class = shop.xpath(".//div[@class='txt']/div[@class='comment']/a[@class='review-num']/b/span/@class")

            for attr in attr_class:
                offset, position = css_and_px_dict[attr]
                index = abs(int(float(offset)))
                position = abs(int(float(position)))
                for key, value in svg_threshold_and_int_dict.items():
                    if position in value:
                        threshold = int(math.ceil(index / 12))
                        number = int(key[threshold - 1])
                        comments_num = comments_num * 10 + number

            print('店铺名称：%s, 点评人数:%s' %(name, comments_num))

    def run(self):
        html = self.request_html(self.start_url)
        css_url = self.get_number_css(html)
        css_content = self.request_html(css_url)
        svg_url = self.get_num_svg(css_content)
        index_and_num_list = self.analysis_svg_file(svg_url)
        css_and_px_dict = self.get_css_and_px_dict(css_content)
        self.analysis_main_page(html, css_and_px_dict, index_and_num_list)


if __name__ == '__main__':
    spider = dianping_spider()
    spider.run()

