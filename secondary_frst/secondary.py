from flask import Flask, request
from message_container import MessageContainer
import random
import time
import os

app = Flask(__name__)

msg_container = MessageContainer()

DELAY = int(os.getenv('DELAY', random.randint(1, 10)))


@app.route('/health')
def index():
    return 'OK'


@app.route('/messages', methods=['POST'])
def save_msg():
    msg = request.get_json()
    time.sleep(DELAY)
    msg_container.append(msg["message"])

    return 'New message successfully added to secondary', 201


@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
