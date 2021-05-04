import telebot
import threading
import parsing
from DataBases import *
import schedule
import time
from mailing_functions import *

bot = telebot.TeleBot('1756290871:AAGj8_apOkmPvisYkES8_mhhYXr-vn3jnFA')
# инициализируем соединение с БД
followers = SQLighter('identifier.sqlite')


# Команда активации подписки
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    if not followers.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        followers.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        followers.update_subscription(message.from_user.id, True)

        bot.send_message(message.chat.id,
                         "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    if not followers.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        followers.add_subscriber(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        followers.update_subscription(message.from_user.id, False)
        bot.send_message(message.chat.id, "Вы успешно отписаны от рассылки.")


def update_information():
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

@bot.message_handler(commands=['parse_wb_new'])
def Top_New(message):
    for i in New.select():
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, i.title + ' ' + i.brand, reply_markup=markup)


@bot.message_handler(commands=['parse_wb_popular'])
def Top_Popular(message):
    for i in Popular.select():
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, i.title + ' ' + i.brand, reply_markup=markup)


@bot.message_handler(commands=['parse_wb_rate'])
def Rate_New(message):
    for i in Rate.select():
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, i.title + ' ' + i.brand, reply_markup=markup)


@bot.message_handler(commands=['parse_wb_price'])
def Price_New(message):
    for i in Price.select():
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, i.title + ' ' + i.brand, reply_markup=markup)


@bot.message_handler(commands=['parse_wb_sale'])
def Sale_New(message):
    for i in Sale.select():
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Ссылка на товар', url=i.link)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, i.title + ' ' + i.brand, reply_markup=markup)


def run_threaded(func):
    job_thread = threading.Thread(target=func)
    job_thread.start()


schedule.every(1).seconds.do(run_threaded, bot.polling)
schedule.every().hour.do(run_threaded, update_information)


def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main_loop()
