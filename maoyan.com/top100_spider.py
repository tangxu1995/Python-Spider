import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}


def get_main_source(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return 'error!'


def parse_item(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('dd')
    for item in items:
        title = item.select('a')[1].text
        rank = item.select('.board-index')[0].text
        star = item.select('.star')[0].text.strip()
        time = item.select('.releasetime')[0].text
        yield {
            'rank': rank,
            'title': title,
            'star': star,
            'time': time
        }


def main(page):
    url = 'http://maoyan.com/board/4?offset={}'.format(page)
    html = get_main_source(url)

    for item in parse_item(html):
        print(item)


if __name__ == '__main__':
    for page in range(0, 10):
        main(page*10)
