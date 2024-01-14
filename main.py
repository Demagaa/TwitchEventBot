import hashlib
import hmac
import json
import os
import requests
from flask import Flask, request

import bot

app = Flask(__name__)

# Notification r`equest headers
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

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

def get_updates():
    # Telegram Bot API endpoint for getting updates
    api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'

    # Make a GET request to the Telegram Bot API
    response = requests.get(api_url)
    response_data = response.json()
    chat_ids = list(set([update['message']['chat']['id'] for update in response_data.get('result', [])]))

    # Return the JSON response from the Telegram Bot API
    return chat_ids


def get_secret():
    return os.environ.get('TWITCH_CLIENT_SECRET')

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
    print("secret " + secret)
    if verify_message(hmac_value, request.headers[TWITCH_MESSAGE_SIGNATURE]):
        print("Signatures match")

        # Get JSON object from body, so you can process the message.
        notification = json.loads(request.data.decode('utf-8'))
        chat_id = get_updates()

        if MESSAGE_TYPE_NOTIFICATION == request.headers[MESSAGE_TYPE]:
            bot.send_notif(notification.get('event', {}).get('broadcaster_user_name'), chat_id)

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

