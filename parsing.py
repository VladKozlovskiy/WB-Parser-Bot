import requests
from bs4 import BeautifulSoup

from config import Beginning, HOST, headers, class_of_item, class_of_title, class_of_brand, class_of_link, page


def check_access(url):
    """Функция которая проверяет доступ к сайту"""
    full_page = requests.get(url, headers=headers)
    if full_page.status_code == 200:
        return True
    return False


def parser(n, criteria):
    """Функция, которая парсит Wildberries  страницу результатов по указанному критерию сортировки"""
    url = Beginning + criteria + page + str(n)
    # получаем разметку страницы
    full_page = requests.get(url, headers=headers)
    if check_access(url):
        soup = BeautifulSoup(full_page.content, 'html.parser')
        # Список в который будем отправлять полученную информвцию
        items = soup.findAll('div', class_=class_of_item)
        res = []
        for item in items:
            res.append(
                {
                    'title': (item.find('span', class_=class_of_title).get_text(strip=True)),
                    'brand': (item.find('strong', class_=class_of_brand).get_text(strip=True)[:-1]).upper(),
                    'link': HOST + item.find('a', class_=class_of_link).get('href')
                }
            )
        return res


def pages_parser(n, criteria):
    """Функция, которая парсит Wildberries  указанное количество страниц результатов  по указанному критерию
    сортировки """
    res = []
    for i in range(n):
        for j in parser(n + 1, criteria):
            res.append(j)
    return res
