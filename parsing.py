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
    """Функция, которая парсит кроссовки с сайта Wildberries  страницу результатов по указанному критерию сортировки
    кроссовок """
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


def pages_parser(number_of_pages, criteria):
    """
    Функция, которая парсит указанное количество страниц сайта с товарами, подходящими критерию выбора пользователя
    :param number_of_pages: количество веб-страниц, на которых содержится результат поиска по критериям
    :param criteria: критерий поиска
    :return: все товары со страниц
    """
    goods = []
    for page_number in range(number_of_pages):
        for product in parser(page_number + 1, criteria):
            goods.append(product)
    return goods
