import parsing
import schedule
import telebot
import threading
import time
from config import token
from DataBases import Rate, New, Price, Popular, Sale

# Вводим токен

bot = telebot.TeleBot(token)
# Словарь для запуска программы
Dict = {'Популярность': Popular.select(), 'Рейтинг': Rate.select(), 'Цена': Price.select(),
        'Самое свежее': New.select(),
        'Самая большая скидка': Sale.select()}


# Обработка команды хелп
@bot.message_handler(commands=["help"])
def tell_instructions(message):
    bot.send_message(message.chat.id,
                     "\tДобрый день! Вас приветствует БотыБот!\n\tЯ умею проверять сайт Wildberries в поисках мужской "
                     "обуви за вас и выдавать вам актуальные предложения отсортированные по таким критериям как: "
                     " Популярность , Самая большая скидка , Рейтинг , Цена , Самое свежее!\n\tЕсли вы хотите "
                     "получить Топ-n товаров в выбранной вами категории, то Вам поможет команда /find_by_criteria . "
                     "\n\tЕсли же хотите получать все товары по указанному Вами критерию(бренд или наименование), "
                     "то Вам подойдет команда /find_top .\n ")


def update_information():
    """Функция обновления базы данных. Перед началом обновления чистим каждую БД, после заполняем и сохраняеи
    информацию """
    for i in New.select():
        i.delete_instance()
    for i in parsing.pages_parser(1, 'new'):
        new = New.create(title=i['title'], brand=i['brand'], link=i['link'])
        new.save()
    for i in Popular.select():
        i.delete_instance()
    for i in parsing.pages_parser(1, 'popular'):
        new_popular = Popular.create(title=i['title'], brand=i['brand'], link=i['link'])
        new_popular.save()
    for i in Rate.select():
        i.delete_instance()
    for i in parsing.pages_parser(1, 'rate'):
        new_rate = Rate.create(title=i['title'], brand=i['brand'], link=i['link'])
        new_rate.save()
    for i in Price.select():
        i.delete_instance()
    for i in parsing.pages_parser(1, 'priceup'):
        new_price = Price.create(title=i['title'], brand=i['brand'], link=i['link'])
        new_price.save()
    for i in Sale.select():
        i.delete_instance()
    for i in parsing.pages_parser(1, 'sale'):
        new_sale = Sale.create(title=i['title'], brand=i['brand'], link=i['link'])
        new_sale.save()


update_information()
'''Обработка команды поиска Топ-n запросов в нужной категории на выбор пользователя'''


@bot.message_handler(commands=['find_top'])
def search_meds(message):
    msg = bot.send_message(message.chat.id,
                           'Введите через пробел критерий, по которому должен быть отсортирован товар, а так же '
                           'количество вариантов, которое хотите получить ')
    bot.register_next_step_handler(msg, search)


def search(message):
    bot.send_message(message.chat.id, 'Ваш запрос обрабатывается')
    data = message.text.split()
    count = 0
    try:
        for i in Dict[data[0]]:
            try:
                if count < int(data[1]):
                    count += 1
                    markup = telebot.types.InlineKeyboardMarkup()
                    btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
                    markup.add(btn_my_site)
                    bot.send_message(message.chat.id, 'Наименование:' + i.title + '\n' + 'Бренд:' + i.brand,
                                     reply_markup=markup)
            except Exception:
                bot.send_message(message.chat.id, 'К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз')
                pass
    except Exception:
        bot.send_message(message.chat.id, 'К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз')
        pass


"""Обработка команды поиска по бренду или наименованию товаров в нужной категории на выбор пользователя"""


@bot.message_handler(commands=['find_by_criteria'])
def search_meds(message):
    msg1 = bot.send_message(message.chat.id,
                            'Введите через пробел критерий, по которому должен быть отсортирован товар, а так же '
                            'бренд или наименование желаемого товара')
    bot.register_next_step_handler(msg1, search1)


def search1(message):
    bot.send_message(message.chat.id, 'Ваш запрос обрабатывается')
    data = message.text.split()
    try:
        for i in Dict[data[0]]:
            markup = telebot.types.InlineKeyboardMarkup()
            btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
            markup.add(btn_my_site)
            if i.brand == data[1].upper() or i.title.lower() == data[1].lower():
                try:
                    bot.send_message(message.chat.id, 'Наименование: ' + i.title + '\n' + 'Бренд: ' + i.brand,
                                     reply_markup=markup)
                except Exception:
                    bot.send_message(message.chat.id, 'К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз')
                    pass
    except Exception:
        bot.send_message(message.chat.id, 'К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз')
        pass


# Чтобы при запуске bot.polling() не перебивал цикл отсчитывания времени для своевренного обновления БД, обновление
# БД и bot.polling()будут работать в разных потоках
def run_threaded(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()


# Задаем период работы функций
schedule.every(1).seconds.do(bot.polling)
schedule.every().hour.do(run_threaded, update_information)


# Исполняемся
def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main_loop()
