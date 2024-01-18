import hashlib
import hmac
import json
import os
import requests
from flask import Flask, request

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

def get_subscribers():
    # Telegram Bot API endpoint for getting updates
    api_url = f'https:/localhost:8082/getSubscribers'

    # Make a GET request to the Telegram Bot API
    response = requests.get(api_url)

    if response.status_code == 200:
        subscribers = response.json()['subscribers']
        return subscribers
        print("List of subscribers:", subscribers)
    else:
        print("Failed to retrieve subscribers. Status code:", response.status_code)


    # Return the JSON response from the Telegram Bot API


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


        subscribers_chat_ids = get_subscribers()


        if MESSAGE_TYPE_NOTIFICATION == request.headers[MESSAGE_TYPE]:
            for subscriber in subscribers_chat_ids:
                # TODO make API to bot microservice
                bot.send_notif(notification.get('event', {}).get('broadcaster_user_name'), subscriber)

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

