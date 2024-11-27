import random
import sqlite3
import telebot

from telebot import types

from api import API
from sql import check_user_registered, register_user, create_db_if_neaded

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

create_db_if_neaded(cursor, conn)

bot = telebot.TeleBot(API)

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton("Как дела?")
    itembtn2 = types.KeyboardButton("Статус")
    markup.add(itembtn1, itembtn2)

    user_id = message.from_user.id
    username = message.from_user.username

    if check_user_registered(user_id, cursor):
        bot.send_message(message.chat.id, "Вы уже зарегистрированы", reply_markup=markup)
    else:
        register_user(user_id, username, cursor, conn)
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы", reply_markup=markup)

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id

    if check_user_registered(user_id, cursor):
        bot.send_message(message.chat.id, f"Вы зарегистрированы. id = {user_id}")
    else:
        bot.send_message(message.chat.id, "Вы не зарегистрированы.")

@bot.message_handler(func=lambda message: message.text == "Как дела?")
def how_are_you(message):
    responses = [
        "Все гуччи",
        "-_-",
        "50/50",
        "Могло быть лучше"
    ]
    if check_user_registered(message.from_user.id, cursor):
        response = random.choice(responses)
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Сначала зарегистрируйтесь, /start.")


if __name__ == "__main__":
    bot.polling(none_stop=True)