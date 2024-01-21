import configparser

import telebot

import user_manager

configparser = configparser.ConfigParser()
configparser.read('config.ini')

BOT_TOKEN = configparser.get('Keys', 'BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

msg = None

subscribers = []


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    print("Received subscription")
    subscribers.append(message.chat.id)
    # Assuming message.chat.id is an integer
    user_manager.save_user_id(message.chat.id)


bot.infinity_polling()
