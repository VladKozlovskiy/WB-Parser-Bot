import requests
from bs4 import BeautifulSoup
from peewee import *



HOST = 'https://www.wildberries.ru'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0'}


def parser(n, criteria):
    url = 'https://www.wildberries.ru/catalog/obuv/muzhskaya?sort=' + criteria + '&page=' + str(n)
    full_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    items = soup.findAll('div', class_='dtList-inner')
    res = []
    for item in items:
        res.append(
            {
                'title': (item.find('span', class_='goods-name c-text-sm').get_text(strip=True)),
                'brand': (item.find('strong', class_='brand-name c-text-sm').get_text(strip=True)[:-1]).upper(),
                'link': HOST + item.find('a', class_='ref_goods_n_p j-open-full-product-card').get('href')
            }
        )
    return res


def pages_parser(n, criteria):
    res = []
    for i in range(n):
        for j in parser(n + 1, criteria):
            res.append(j)
    return res


