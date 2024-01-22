import configparser

import telebot

import user_manager

configparser = configparser.ConfigParser()
configparser.read('config.ini')

BOT_TOKEN = configparser.get('Keys', 'BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

msg = None


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    response = user_manager.save_user_id(message.chat.id)
    bot.reply_to(message, response)



@bot.message_handler(commands=['unsubscribe'])
def subscribe(message):
    response = user_manager.remove_user_id(message.chat.id)
    bot.reply_to(message, response)


bot.infinity_polling()
