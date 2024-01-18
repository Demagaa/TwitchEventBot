import telebot
import requests
import os

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

msg = None

subscribers = []
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    print("Received subscription")
    api_url = f'http://localhost:8082/createSubscribtion'
    subscribers.append(message.chat.id)
    # Assuming message.chat.id is an integer
    data_dict = {'chat_id': message.chat.id}

    response = requests.post(api_url, json=data_dict)
    print(response)

def send_notif(nickname, chat_ids):
    for chat_id in chat_ids:
        bot.send_message(chat_id, f"{nickname} just went online")

bot.infinity_polling()

