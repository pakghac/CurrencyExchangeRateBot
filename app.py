import telebot
from config import TOKEN, currencies
from extensions import APIException, Converter
from bot_message import *
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message, start_message)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    bot.reply_to(message, help_message)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны валюты:\n'
    сurrencies_str = '\n'.join(currencies.keys())
    text += сurrencies_str
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров! Справка: /help')
        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        bot.reply_to(message, answer)

bot.polling(none_stop=True)