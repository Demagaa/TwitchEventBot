import telebot
import requests

bot = telebot.TeleBot('6667630731:AAFRdAj3DcdvL5LPECZIQzAqKrov6EhT9Nw')

msg = None

@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    print("Received subscription")
    api_url = f'http://localhost:8082/createSubscribtion'
    # Assuming message.chat.id is an integer
    data_dict = {'chat_id': message.chat.id}

    response = requests.post(api_url, json=data_dict)
    print(response)

def send_notif(nickname, chat_ids):
    for chat_id in chat_ids:
        bot.send_message(chat_id, f"{nickname} just went online")

bot.infinity_polling()

