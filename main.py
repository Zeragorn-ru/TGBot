import telebot
import random
import requests
from config import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

bot = telebot.TeleBot(BOT_API)


@bot.message_handler(commands=['start'])
def start(message):
    with open('./test.png', 'rb') as img:
        text = "test massage"

        markup = types.InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="Button test", callback_data="start_but"),InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))


        bot.send_photo(message.chat.id, img, caption=text, reply_markup=markup)


if __name__ == '__main__':
    print("Bot was started")
    bot.polling(none_stop=True)