"""Файл с запуском бота"""
import schedule
import telebot
import threading
import time

import parsing
from config import BD_dict, token, User_message_dict

# Вводим токен

bot = telebot.TeleBot(token)


# Обработка команды хелп
@bot.message_handler(commands=["help"])
def tell_instructions(message):
    bot.send_message(message.chat.id,
                     "\tДобрый день! Вас приветствует БотыБот!\n Я умею проверять сайт Wildberries в поисках мужской "
                     "обуви за вас и выдавать вам актуальные предложения отсортированные по таким критериям как: "
                     " Популярность , Скидка , Рейтинг , Цена , Свежее!\n\tЕсли вы хотите "
                     "получить Топ-n товаров в выбранной вами категории, то Вам поможет команда /find_top . "
                     "\n\tЕсли же хотите получать все товары по указанному Вами критерию(бренд или наименование), "
                     "то Вам подойдет команда /find_by_criteria .\n ")


def update_db(cretiria):
    """Функция обновления базы данных. Перед началом обновления чистим каждую БД, после заполняем и сохраняеи
        информацию """
    for item in BD_dict[cretiria].select():
        item.delete_instance()
    for item in parsing.pages_parser(1, cretiria):
        new = BD_dict[cretiria].create(title=item["title"], brand=item["brand"], link=item["link"])
        new.save()


def update_information():
    """Функция обновления баз данных. """
    for item in BD_dict.keys():
        update_db(item)


update_information()
'''Обработка команды поиска Топ-n запросов в нужной категории на выбор пользователя'''


@bot.message_handler(commands=["find_top"])
def search_meds(message):
    msg_top = bot.send_message(message.chat.id,
                               "Введите через пробел критерий, по которому должен быть отсортирован товар, а так же "
                               "количество вариантов, которое хотите получить. \n Пример: Популярность 10 ")
    bot.register_next_step_handler(msg_top, search_top)


def search_top(message):
    bot.send_message(message.chat.id, "Ваш запрос обрабатывается")
    data = message.text.split()
    count = 0
    try:
        for item in User_message_dict[data[0]]:
            try:
                if count < int(data[1]):
                    count += 1
                    markup = telebot.types.InlineKeyboardMarkup()
                    btn_my_site = telebot.types.InlineKeyboardButton(text="Ссылка на товар", url=item.link)
                    markup.add(btn_my_site)
                    bot.send_message(message.chat.id, f"Наименование: {item.title}  \n Бренд: {item.brand}",
                                     reply_markup=markup)
            except Exception:
                bot.send_message(message.chat.id, "К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз")
                pass
        bot.send_message(message.chat.id, "Ваш запрос обработан.")
    except Exception:
        bot.send_message(message.chat.id, "К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз")
        pass


"""Обработка команды поиска по бренду или наименованию товаров в нужной категории на выбор пользователя"""


@bot.message_handler(commands=["find_by_criteria"])
def search_meds_criteria(message):
    msg_creteria = bot.send_message(message.chat.id,
                                    "Введите через пробел критерий, по которому должен быть отсортирован товар, "
                                    "а так же "
                                    "бренд или наименование желаемого товара. \n Пример: Популярность кроссовки.")
    bot.register_next_step_handler(msg_creteria, search_criteria)


def search_criteria(message):
    bot.send_message(message.chat.id, "Ваш запрос обрабатывается")
    data = message.text.split()
    try:
        for item in User_message_dict[data[0]]:
            markup = telebot.types.InlineKeyboardMarkup()
            btn_my_site = telebot.types.InlineKeyboardButton(text="Ссылка на товар", url=item.link)
            markup.add(btn_my_site)
            if item.brand == data[1].upper() or item.title.lower() == data[1].lower():
                try:
                    bot.send_message(message.chat.id, f"Наименование: {item.title}  \n Бренд: {item.brand}",
                                     reply_markup=markup)
                except Exception:
                    bot.send_message(message.chat.id, "К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз")
                    pass
        bot.send_message(message.chat.id,
                         "Поиск закончен. Если вы ничего не получили, то, к сожалению, такого товара нет.")
    except Exception:
        bot.send_message(message.chat.id, "К сожалению, Вы некорректно ввели данные:( Попробуйте еще раз")
        pass


# Чтобы при запуске bot.polling() не перебивал цикл отсчитывания времени для своевренного обновления БД, обновление
# БД и bot.polling()будут работать в разных потоках
def run_threaded(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()


@bot.message_handler(content_types=["text"])
def answer(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, пожалуйста, введите команду")


# Задаем период работы функций
bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
schedule.every().hour.do(run_threaded, update_information)


# Исполняемся
def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__bot__":
    main_loop()
