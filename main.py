BOT_VERSION = "Beta 1.1.1"

#Проверка наличия конфига

try:
    with open("config.py","r"):
        print("Config status: found ")
except FileNotFoundError:
    with open("config.py","w+") as config:
        config.write(f"BOT_API=\"{input("Введите api бота: ")}\"")

#импорт библиотек
import telebot
import asyncio

import requests
from config import *
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

bot = telebot.TeleBot(BOT_API)

@bot.message_handler(commands=['start'])
def start(message):
    with open('./test.png', 'rb') as img:
        text = "Добро пожаловать в нашего телеграмм бота для оплаты ЖКХ \nЭтот бот поможет вам:\n · ййцц"
        markup = types.InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="Button test", callback_data="start_but"),InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.row(InlineKeyboardButton(text="inf", callback_data="inf"),InlineKeyboardButton(text="Профиль", callback_data="Profile"),InlineKeyboardButton(text="Поддержка", callback_data="pod"))

        bot.send_photo(message.chat.id, img, caption=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "inf")
def inf(call):
    with open("./test_2.png","rb") as img:
        markup = types.InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="<- назад",callback_data="main_menu"))
        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=f"Ваш id: {call.message.chat.id}"),chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def main_menu(call):
    with open('./test.png', 'rb') as img:
        text = "Добро пожаловать в нашего телеграмм бота для оплаты ЖКХ \nЭтот бот поможет вам:\n · ййцц"
        markup = types.InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton(text="Button test", callback_data="start_but"),InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.add(InlineKeyboardButton(text="Button test", callback_data="start_but"))
        markup.row(InlineKeyboardButton(text="inf", callback_data="inf"),InlineKeyboardButton(text="Профиль", callback_data="Profile"),InlineKeyboardButton(text="Поддержка", callback_data="pod"))

        bot.edit_message_media(types.InputMediaPhoto(media=img, caption=f"Добро пожаловать в нашего телеграмм бота для оплаты ЖКХ \nЭтот бот поможет вам:\n · ййцц"), reply_markup=markup,chat_id=call.message.chat.id,message_id=call.message.message_id)

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