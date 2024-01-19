import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
subscribers = []


@app.route('/getSubscribers', methods=['GET'])
def getSubscribers():
    return jsonify(subscribers)


@app.route('/createSubscribtion', methods=['POST'])
def createSubscribtion():
    # Ensure that the request contains JSON data
    if request.is_json:
        try:
            data = request.get_json()
            # print(data)
            chat_id = data.get('chat_id')

            if chat_id is not None and chat_id not in subscribers:
                subscribers.append(chat_id)
                print(subscribers)
                return jsonify({'message': 'Subscription created successfully'})
            else:
                return jsonify({'message': 'Invalid or duplicate chat_id'}), 400
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    else:
        return jsonify({'message': 'Invalid request format'}), 400


if __name__ == '__main__':
    app.run(port=8082)
