import os
import telebot
import hashlib
import hmac
import json
import twitchio
from flask import Flask, request, jsonify
import secrets

# bot = telebot.TeleBot('6667630731:AAFRdAj3DcdvL5LPECZIQzAqKrov6EhT9Nw')
#
#
# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#

# bot.infinity_polling()

app = Flask(__name__)

# Notification request headers
TWITCH_MESSAGE_ID = 'Twitch-Eventsub-Message-Id'.lower()
TWITCH_MESSAGE_TIMESTAMP = 'Twitch-Eventsub-Message-Timestamp'.lower()
TWITCH_MESSAGE_SIGNATURE = 'Twitch-Eventsub-Message-Signature'.lower()
MESSAGE_TYPE = 'Twitch-Eventsub-Message-Type'.lower()

# Notification message types
MESSAGE_TYPE_VERIFICATION = 'webhook_callback_verification'
MESSAGE_TYPE_NOTIFICATION = 'notification'
MESSAGE_TYPE_REVOCATION = 'revocation'

# Prepend this string to the HMAC that's created from the message
HMAC_PREFIX = 'sha256='

def get_secret():
    # TODO: Get secret from secure storage. This is the secret you pass
    # when you subscribed to the event.
    return ''

# Build the message used to get the HMAC.
def get_hmac_message(request):
    return (request.headers[TWITCH_MESSAGE_ID] +
            request.headers[TWITCH_MESSAGE_TIMESTAMP] +
            request.data.decode('utf-8'))

# Get the HMAC.
def get_hmac(secret, message):
    return HMAC_PREFIX + hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

# Verify whether our hash matches the hash that Twitch passed in the header.
def verify_message(hmac, verify_signature):
    return hmac == verify_signature


@app.route('/streamstart', methods=['POST'])
def streamstart():
    secret = get_secret()
    message = get_hmac_message(request)
    hmac_value = get_hmac(secret, message)

    if verify_message(hmac_value, request.headers[TWITCH_MESSAGE_SIGNATURE]):
        print("Signatures match")

        # Get JSON object from body, so you can process the message.
        notification = json.loads(request.data.decode('utf-8'))

        if MESSAGE_TYPE_NOTIFICATION == request.headers[MESSAGE_TYPE]:
            # TODO: Do something with the event's data.
            print(f"Event type: {notification['subscription']['type']}")
            print(json.dumps(notification['event'], indent=4))
            return '', 204
        elif MESSAGE_TYPE_VERIFICATION == request.headers[MESSAGE_TYPE]:
            return notification['challenge'], 200, {'Content-Type': 'text/plain'}
        elif MESSAGE_TYPE_REVOCATION == request.headers[MESSAGE_TYPE]:
            print(f"{notification['subscription']['type']} notifications revoked!")
            print(f"Reason: {notification['subscription']['status']}")
            print(f"Condition: {json.dumps(notification['subscription']['condition'], indent=4)}")
            return '', 204
        else:
            print(f"Unknown message type: {request.headers[MESSAGE_TYPE]}")
            return '', 204
    else:
        print('403')  # Signatures didn't match.
        return '', 403

if __name__ == '__main__':
    app.run(port=443)

