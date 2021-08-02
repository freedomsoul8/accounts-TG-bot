from telebot import types
import sqlite3
file = 'db.sqlite3'

try:
    connection = sqlite3.connect(file, check_same_thread=False )
    cursor = connection.cursor()
except sqlite3.Error as e:
    print(e)


def add_order(name, id, cost, date):
    sql = "INSERT INTO adminTG_order (order_id, order_name, order_cost, order_date) VALUES (?,?,?,?)"
    val = (name, id, cost, date)
    cursor.execute(sql,val)
    connection.commit()




def table_select_price(name):
    sql = f"SELECT price FROM adminTG_category WHERE name =? "
    from accmaster.bot.app import purchase
    value = (purchase.name,)
    cursor.execute(sql, value)
    purchase.price = cursor.fetchone()
    cursor.close()
    return purchase.price[0]




def markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    x = cursor.execute("SELECT name, id, price FROM adminTG_category")
    categories = cursor.fetchall()
    for name, id, price in categories:
        markup.add(types.KeyboardButton(text=f"{name} "))
    return markup


def create_tables():
    cursor.execute("SELECT name FROM adminTG_category")
    categories = cursor.fetchall()
    for name in categories:
        from accmaster.bot.app import gc

        sheet = gc.open(title='accmaster')
        try:
            wks = sheet.add_worksheet(title=f'{name[0]}')
            print(name[0])
            wks.update_values('A1:B1', [['name'],['password']])
        except:
            pass