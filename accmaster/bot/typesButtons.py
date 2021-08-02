import telebot
from telebot import types
import pandas as pd
import xlwings as xl




#mainmenu
mainmenuKB = types.InlineKeyboardMarkup()
buyB = types.InlineKeyboardButton(text='Купить Аккаунты', callback_data="buyB")
mainmenuKB.add(buyB)

#backmainmenu
backM =types.InlineKeyboardMarkup()
back = types.InlineKeyboardButton(text='Назад', callback_data='back')
backM.add(back)

#buymenu
buymenuKB = types.InlineKeyboardMarkup()
orderB = types.InlineKeyboardButton(text='Купить!', callback_data='BuyA')
buymenuKB.add(orderB,back)



