from  config import *
import telebot
from telebot import types

TOKEN = "Ваш_токен_бота"
bot = telebot.TeleBot(BOT_API)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Отправляем сообщение с медиа (картинка) и текстом
    photo = open("test.png", "rb")  # Замените на путь к своему изображению
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Нажми меня!", callback_data="button_pressed")
    markup.add(button)

    sent_message = bot.send_photo(
        message.chat.id,
        photo,
        caption="Это сообщение с медиа и текстом",  # Текст в сообщении
        reply_markup=markup
    )

    # Сохраняем message_id, чтобы редактировать его позже
    print(f"Sent message ID: {sent_message.message_id}")  # Для логирования


# Обработчик callback от inline кнопки
@bot.callback_query_handler(func=lambda call: call.data == "button_pressed")
def button_pressed(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    # Логируем callback данные
    print(f"Callback data received: {call.data}")
    print(f"Message ID to edit: {message_id}")

    # Проверяем, если сообщение содержит текст
    if call.message.text:
        # Редактируем только текст
        bot.edit_message_text(
            "Текст сообщения был изменен после нажатия на кнопку!",
            chat_id=chat_id,
            message_id=message_id
        )
        print("Text updated successfully.")

    # Редактируем медиа (изображение)
    photo = open("test.png", "rb")  # Новый путь к изображению
    bot.edit_message_media(
        types.InputMediaPhoto(photo, caption="Новый текст после редактирования."),
        chat_id=chat_id,
        message_id=message_id
    )
    print("Media updated successfully.")

    # Отправляем ответ на нажатие кнопки
    bot.answer_callback_query(call.id, "Текст и медиа изменены!")


bot.polling()
