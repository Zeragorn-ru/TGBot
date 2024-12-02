# -*- coding: windows-1251 -*-
# импорт библиотек
import sqlite3
import telebot
import requests
import asyncio
from config import *
from lang_file import *
from database import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import datetime

BOT_VERSION = "Beta 7a"

# Проверка наличия конфига

try:
    with open("config.py", "r"):
        print("Config status: Success ")
except FileNotFoundError:
    with open("config.py", "w+") as config:
        config.write(f"BOT_API=\"{input("Enter bot api: ")}\"\nlang=\"{input("select lang(en/ru): ")}\"")

try:
    with open(BASE_NAME, "r"):
        print("Data status: Success ")
except FileNotFoundError:
    with sqlite3.connect(BASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users ("user_name"	TEXT, "currency"	TEXT, "user_id"	INTEGER, "admin" INTEGER)
        """)
        conn.commit()

bot = telebot.TeleBot(BOT_API)

def tr(key):
    # Получаем шаблон строки по ключу
    template = lang_list[lang][key]

    if template is None:
        return f"Шаблон с ключом '{key}' не найден!"

    # Используем eval() для подстановки значений глобальных переменных
    try:
        return template.format(**globals())  # Использование globals() для подстановки глобальных переменных
    except KeyError as e:
        print(f"Ошибка: переменная {e} не найдена.")


@bot.message_handler(commands=['start'])
def start(message):
    global mes
    mes = message
    with open('./test.png', 'rb') as img:
        text = tr("main_tx")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("caog_bt"), callback_data="catalog"))
        markup.row(InlineKeyboardButton(text=tr("info_bt"), callback_data="inf"),
                   InlineKeyboardButton(text=tr("prof_bt"), callback_data="Profile"),
                   InlineKeyboardButton(text=tr("supp_bt"), callback_data="support"))

        bot.send_photo(message.chat.id, img, caption=text, reply_markup=markup)
        add_user(message)
        add_remind(message, "2024.12.01 12:30:00", "test text")

@bot.callback_query_handler(func=lambda call: call.data == "inf")
def inf(call):
    with open("./test_2.png", "rb") as img:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("back_bt"), callback_data="main_menu"))
        bot.edit_message_media(
            types.InputMediaPhoto(media=img, caption=f"Bot version: {BOT_VERSION}\nMS_ID: {call.message.message_id}"),
            chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu(call):
    with open('./test.png', 'rb') as img:
        text = tr("main_tx")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("caog_bt"), callback_data="catalog"))
        markup.row(InlineKeyboardButton(text=tr("info_bt"), callback_data="inf"),
                   InlineKeyboardButton(text=tr("prof_bt"), callback_data="profile"),
                   InlineKeyboardButton(text=tr("supp_bt"), callback_data="support"))

        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=text),
                               reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "support")
def support(call):
    with open("./test_2.png", "rb") as img:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("back_bt"), callback_data="main_menu"))
        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=tr("supp_tx")), chat_id=call.message.chat.id,
                               message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "profile")
def profile(call):
    global call_
    call_ = call
    with open("./test_2.png", "rb") as img:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("back_bt"), callback_data="main_menu"))
        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=tr("prof_tx")), chat_id=call.message.chat.id,
                               message_id=call.message.message_id, reply_markup=markup)


# Контроль через консоль
async def console_control():
    while True:
        command = await asyncio.to_thread(input, "> ")
        if command.lower() == "test":
            bot.send_message(chat_id="5874936084", text="5874936084")
            print("massage")
        elif command == "stop":
            print("Bot stopped")
            bot.stop_polling()
            break
        else:
            print("unknown command")


# главная функция
async def main():
    bot_task = asyncio.to_thread(bot.infinity_polling)
    console_task = console_control()
    await asyncio.gather(bot_task, console_task)


if __name__ == '__main__':
    print("Bot was started")
    asyncio.run(main())
