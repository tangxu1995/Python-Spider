import requests_html


url = 'http://quotes.toscrape.com/js/page/{}'
url_lists = [url.format(page) for page in range(1, 11)]


session = requests_html.HTMLSession()

for url in url_lists:

    print('*'*30)

    print('crawling {}'.format(url))

    print('*' * 30)

    r = session.get(url)

    r.html.render()

    items = r.html.xpath('//div[@class="container"]/div')

    for item in items[1:]:

        text = item.xpath('.//span[1]/text()')[0]
        author = ''.join(item.xpath('.//span[2]//text()'))
        tags = ''.join(item.xpath(".//div//text()")[3:])
        print(text, author, tags)