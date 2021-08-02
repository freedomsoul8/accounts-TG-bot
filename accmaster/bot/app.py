import flask
from flask import Flask
import telebot
from telebot import types
import typesButtons as tp
import time
import requests
from wayforpay.utils import generate_signature
import datetime
from datetime import datetime, timezone
import random
import pygsheets
from accmaster.adminkaTG.db_workers import add_order, table_select_price, markup

bot = telebot.TeleBot('1827521176:AAEY7xTObJ1e9A5WDkJb5N7XrtGz4f_B5ys')
bot.set_webhook('https://0acb3f07e3f4.ngrok.io')
app = Flask(__name__)
gc = pygsheets.authorize(service_account_file='service_account.json')

orders = []
purchase_data = {}


class purchase:
    name = ''
    count = 0
    price = 0
    date = 0
    order = 0
    cost = 0

    def __init__(self, ):
        self.count = 0
        self.name = ''
        self.price = 0
        self.date = 0
        self.order = 0
        self.cost = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!', reply_markup=tp.mainmenuKB)


class category:
    def __init__(self):
        self.categoryName = ''
        self.categoryprice = 0


@bot.message_handler(commands=['buy'])
def category(message):

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
        ordernew = str(random.randrange(0, 99999999))
        order_date = int(datetime.now().replace(tzinfo=timezone.utc).timestamp())
        purchase.order = ordernew + "5"
        signature_data = f"t_me500;t.me/accmaster_bot;{purchase.order};{order_date};{purchase.cost};{currency};{productName};{count};{productPrice}"
        signature = generate_signature(merchant_key, signature_data)
        params = {
            'transactionType': "CREATE_INVOICE",
            'merchantAccount': merchant_account,
            'merchantDomainName': merchant_domain_name,
            'merchantSignature': signature,
            'apiVersion': 1,
            'orderReference': purchase.order,
            'orderDate': order_date,
            'amount': purchase.cost,
            'currency': currency,
            'productName': [productName],
            'productPrice': [productPrice],
            'productCount': [count],
            'orderTimeout': 10
        }

        response = requests.post("https://api.wayforpay.com/api", json=params).json()
        invoiceUrl = response["invoiceUrl"]
        print(response)

        pay = types.InlineKeyboardMarkup()
        payB = types.InlineKeyboardButton(text='Купить!', url=invoiceUrl)
        pay.add(payB)

        add_order(name=str(productName), id=int(purchase.order), cost=int(purchase.cost), date=int(purchase.date))
        bot.send_message(message.chat.id, text=f'Заказ №: {purchase.order}\nДата: {time.ctime(order_date)} UTC',
                         reply_markup=pay)



    except:
        reasonCode = response["reasonCode"]
        reason = response["reason"]
        bot.send_message(message.chat.id, text=f'Ошибка! \nКод ошибки - {reasonCode} ({reason})',
                         reply_markup=tp.mainmenuKB)

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

    responseVE = requests.post("https://api.wayforpay.com/api", json=data).json()

    while responseVE["transactionStatus"] != "Approved":
        if message.text == 'Отмена':
            print(111)
            break
        responseVE = requests.post("https://api.wayforpay.com/api", json=data).json()

        print(responseVE)

        time.sleep(30)


    else:
        if responseVE["transactionStatus"] == "Declined":
            bot.send_message(message.chat.id,
                             text=f'Оплата не прошла\nКод ошибки:{responseVE["Reason"]}\n{responseVE["ReasonCode"]} \nЗаказ №:{purchase.order}')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == 'buyB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Чтобы приобрести аккаунты, введите команду /buy', reply_markup=tp.backM)
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Привет!',
                              reply_markup=tp.mainmenuKB)


@app.route("/", methods=["POST"])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


if __name__ == '__main__':
    app.run()
