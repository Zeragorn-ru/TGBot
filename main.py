BOT_VERSION = "Beta 3a"

#Проверка наличия конфига

try:
    with open("config.py","r"):
        print("Config status: found ")
except FileNotFoundError:
    with open("config.py","w+") as config:
        config.write(f"BOT_API=\"{input("Enter bot api: ")}\"\nlang=\"{input("select lang(en/ru): ")}\"")



#импорт библиотек
import telebot
import asyncio
import json
import requests
from config import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

bot = telebot.TeleBot(BOT_API)

def load_translation(lang):
    try:
        with open(f"./lang/{lang}.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: файл перевода для языка {lang} не найден.")
        return {}

def tr(key):
    translations = load_translation(lang)
    return translations.get(key, key)

@bot.message_handler(commands=['start'])
def start(message):
    with open('./test.png', 'rb') as img:
        text = tr("main_tx")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("caog_bt"), callback_data="catalog"))
        markup.row(InlineKeyboardButton(text=tr("info_bt"), callback_data="inf"),InlineKeyboardButton(text=tr("prof_bt"), callback_data="Profile"),InlineKeyboardButton(text=tr("supp_bt"), callback_data="support"))

        bot.send_photo(message.chat.id, img, caption=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "inf")
def inf(call):
    with open("./test_2.png","rb") as img:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("back_bt"),callback_data="main_menu"))
        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=f"Bot version: {BOT_VERSION}\nMS_ID: {call.message.message_id}"),chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu(call):
    with open('./test.png', 'rb') as img:
        text = tr("main_tx")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("caog_bt"), callback_data="catalog"))
        markup.row(InlineKeyboardButton(text=tr("info_bt"), callback_data="inf"),InlineKeyboardButton(text=tr("prof_bt"), callback_data="profile"),InlineKeyboardButton(text=tr("supp_bt"), callback_data="support"))

        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=f"Добро пожаловать в нашего телеграмм бота для оплаты ЖКХ \nЭтот бот поможет вам:\n · ййцц"), reply_markup=markup,chat_id=call.message.chat.id,message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == "support")
def inf(call):
    with open("./test_2.png","rb") as img:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=tr("back_bt"),callback_data="main_menu"))
        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=tr("supp_tx")),chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)


#Контроль через консоль
async def console_control():
    while True:
        command = await asyncio.to_thread(input, "> ")
        if command.lower() == "test command":
            bot.send_message(chat_id="5874936084",text="5874936084")
            print("massage")
        elif command == "stop":
            print("Bot stopped")
            bot.stop_polling()
            break
        else:
            print("unknown command")

#главная функция
async def main():
    bot_task = asyncio.to_thread(bot.infinity_polling)
    console_task = console_control()
    await asyncio.gather(bot_task, console_task)

if __name__ == '__main__':
    print("Bot was started")
    asyncio.run(main())