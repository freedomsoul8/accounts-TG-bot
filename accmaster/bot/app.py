import telebot
from telebot import types
import sqlite3
import time
import requests
from wayforpay.utils import generate_signature
import datetime
from datetime import datetime, timezone
import random
import pygsheets

import pathlib
from pathlib import Path
from accmaster.bot.typesButtons import mainmenuKB, backM

bot = telebot.TeleBot('1827521176:AAEY7xTObJ1e9A5WDkJb5N7XrtGz4f_B5ys')
p = Path(__file__).resolve().parent.parent / 'adminkaTG' / 'db.sqlite3'
print(p)
connection = sqlite3.connect(p, check_same_thread=False)

gc = pygsheets.authorize(service_account_file='service_account.json')
# gcc = pygsheets.worksheet.Worksheet.get_row()
orders = []
purchase_data = {}


class purchase:
    name = ''
    count = 0
    price = 0
    date = 0
    order = '0'
    cost = 0

    def __init__(self, ):
        self.count = 0
        self.name = ''
        self.price = 0
        self.date = 0
        self.order = '0'
        self.cost = 0


def save_data(message_id):
    c = connection.cursor()
    sql = "INSERT INTO users (user_id) VALUES (?)"
    val = (message_id,)
    c.execute(sql, val)
    connection.commit()


def send_message():
    chats = get_chat_id()
    for chat_id in chats:
        try:
            bot.send_message(chat_id=chat_id[0], text='Подлил аккаунтов в магаз')
        except:

            pass


def get_chat_id():
    c = connection.cursor()
    c.execute("SELECT user_id FROM users")
    chat_ids = c.fetchall()
    c.close()
    return chat_ids


def create_tables(message):
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM adminTG_category")
    categories = cursor.fetchall()

    for name in categories:

        sheets = gc.spreadsheet_titles(query=None)
        if name[0] in sheets:
            bot.send_message(chat_id=message, text=f'{name[0]} ........is alredy exist')
            print(f'{name[0]} ........is alredy exist')
            pass
        else:

            newsheet = gc.create(title=name[0])
            bot.send_message(chat_id=message, text=f'{name[0]} ........created')
            print(f'{name[0]} ........created')





def markup():
    cursor = connection.cursor()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    x = cursor.execute("SELECT name, id, price FROM adminTG_category")
    categories = cursor.fetchall()
    for name, id, price in categories:
        markup.add(types.KeyboardButton(text=f"{name} "))
    return markup


def add_order(name, id, cost, date):
    cursor = connection.cursor()
    sql = "INSERT INTO adminTG_order (order_id, order_name, order_cost, order_date) VALUES (?,?,?,?)"
    val = (name, id, cost, date)
    cursor.execute(sql, val)
    connection.commit()


def table_select_price(name):
    cursor = connection.cursor()
    sql = f"SELECT price FROM adminTG_category WHERE name =? "

    value = (purchase.name,)
    cursor.execute(sql, value)
    purchase.price = cursor.fetchone()
    cursor.close()
    return purchase.price[0]


admins = ['463362670']

admin_menu = types.InlineKeyboardMarkup()
add_categories = types.InlineKeyboardButton(text='Добавить таблицы excel из бд ', callback_data='add_t')
send_msg = types.InlineKeyboardButton(text='Отправить сообщение', callback_data='send_msg_f_a')
admin_menu.add(add_categories).add(send_msg)


@bot.message_handler(commands=['admin'])
def admin_msg(message):
    if message.chat.id == 463362670:
        bot.send_message(message.chat.id, text='Привет админ!', reply_markup=admin_menu)
    else:
        print(message.chat.id)
        pass


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!', reply_markup=mainmenuKB)
    try:
        save_data(message_id=message.chat.id)
    except:
        pass


@bot.message_handler(commands=['buy'])
def category(message):
    create_tables()
    msg = bot.send_message(message.chat.id, text='Выберите категорию!', reply_markup=markup())
    bot.register_next_step_handler(msg, choose)


def choose(message):
    purchase.name = message.text
    msg = bot.send_message(message.chat.id, text='Введите количество аккаунтов, сколько хотите купить')

    bot.register_next_step_handler(msg, buy)


def buy(message):
    purchase.count = message.text
    try:
        merchant_key = "ec394cff2f91ff7a0059779674b60ce2c3892a20"
        merchant_account = "t_me500"
        merchant_domain_name = "t.me/accmaster_bot"
        currency = "UAH"
        count = int(purchase.count)
        productName = purchase.name
        productPrice = int(table_select_price(name=purchase.name))
        purchase.cost = count * productPrice
        purchase.order = str(random.randrange(0, 9999999999999))
        purchase.date = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())

        signature_data = f"t_me500;t.me/accmaster_bot;{purchase.order};{purchase.date};{purchase.cost};{currency};{productName};{count};{productPrice}"
        signature = generate_signature(merchant_key, signature_data)
        params = {
            'transactionType': "CREATE_INVOICE",
            'merchantAccount': merchant_account,
            'merchantDomainName': merchant_domain_name,
            'merchantSignature': signature,
            'apiVersion': 1,
            'orderReference': purchase.order,
            'orderDate': purchase.date,
            'amount': purchase.cost,
            'currency': currency,
            'productName': [productName],
            'productPrice': [productPrice],
            'productCount': [count],
            'orderTimeout': 25
        }

        response = requests.post("https://api.wayforpay.com/api", json=params).json()
        invoiceUrl = response["invoiceUrl"]
        print(response)
        pay = types.InlineKeyboardMarkup()
        payB = types.InlineKeyboardButton(text='Купить!', url=invoiceUrl)
        pay.add(payB)
        print(1)

        bot.send_message(message.chat.id, text=f'Заказ №: {purchase.order}\nДата: {time.ctime(purchase.date)} UTC',
                         reply_markup=pay)



    except:

        reasonCode = response["reasonCode"]
        reason = response["reason"]
        bot.send_message(message.chat.id, text=f'Ошибка! \nКод ошибки - {reasonCode} ({reason})',
                         reply_markup=mainmenuKB)
    add_order(name=purchase.name, id=purchase.order, date=datetime.fromtimestamp(purchase.date), cost=purchase.cost)
    merchant_key = "ec394cff2f91ff7a0059779674b60ce2c3892a20"
    merchant_account = "t_me500"
    signature_data = f"t_me500;{purchase.order}"

    data = {
        "transactionType": "CHECK_STATUS",
        "merchantAccount": merchant_account,
        "orderReference": purchase.order,
        "merchantSignature": generate_signature(merchant_key, signature_data),
        "apiVersion": 1
    }
    responseV = requests.post("https://api.wayforpay.com/api", json=data).json()
    print(responseV)
    responseVE = requests.post("https://api.wayforpay.com/api", json=data).json()

    while responseVE["transactionStatus"] != "Approved":

        responseVE = requests.post("https://api.wayforpay.com/api", json=data).json()

        print(responseVE)
        if responseVE["transactionStatus"] == "Approved":
            bot.send_message(chat_id=message.chat.id, text='Оплата прошла!')

        time.sleep(2)


    else:
        if responseVE["transactionStatus"] == "Declined":
            bot.send_message(message.chat.id,
                             text=f'Оплата не прошла\nКод ошибки:{responseVE["Reason"]}\n{responseVE["ReasonCode"]} \nЗаказ №:{purchase.order}')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'buyB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Чтобы приобрести аккаунты, введите команду /buy', reply_markup=backM)
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Привет!',
                              reply_markup=mainmenuKB)
    if call.data == 'add_t':
        create_tables(message=call.message.chat.id)
        bot.send_message(chat_id=call.message.chat.id, text='Админ панель', reply_markup=admin_menu)
    if call.data == 'send_msg_f_a':
        send_message()




if __name__ == '__main__':
    bot.polling(none_stop=True)

