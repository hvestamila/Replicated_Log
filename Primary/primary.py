from flask import Flask, request
import requests
from .message_container import MessageContainer

app = Flask(__name__)

msg_container = MessageContainer()

# primary port = 5000
secondary_frst_endpoint = 'http://localhost:6000/messages'
secondary_scnd_endpoint = 'http://localhost:7000/messages'


@app.route('/messages', methods=['POST'])
def save_msg():
    msg = request.get_json()
    r_frst = requests.post(secondary_frst_endpoint, json=msg)
    r_scnd = requests.post(secondary_scnd_endpoint, json=msg)
    if r_frst.status_code == 201 & r_scnd.status_code == 201:
        msg_container.append(msg["message"])
    # Secondary nodes will have the same code
    # but they will only have request.get_json() and append

    # to test that the replication is blocking, introduce the delay/sleep on the Secondary
    # you can use time.sleep(5) to do that
    return 'New message successfully added', 201


@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200
