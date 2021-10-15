from flask import Flask, request
from message_container import MessageContainer
import requests
import threading

app = Flask(__name__)

msg_container = MessageContainer()

# primary port = 5000
endpoints = list()
endpoints.append('http://localhost:6000/messages')
endpoints.append('http://localhost:7000/messages')
ReplicateCount = 0

def ReplicateMessage(secondaryEndpoint, msg):
    global ReplicateCount
    resultOfResponce = requests.post(secondaryEndpoint, json=msg)
    if (resultOfResponce.ok == True): ReplicateCount = ReplicateCount + 1

def ProcessRequest(MsgTest):
    global ReplicateCount
    ReplicateCount = 0
    treads = list()
    for endpoint in endpoints:
        treads.append(threading.Thread(target=ReplicateMessage, args=(endpoint, MsgTest)))

    for t in treads:
        t.start()

    for t2 in treads:
        t2.join()

    return ReplicateCount


@app.route('/')
def index():
    return "hello world"

@app.route('/messages', methods=['POST'])
def save_msg():
    msg = request.get_json()
    port = request.server[1]
    res = ProcessRequest(msg)

    if res == len(endpoints):
        msg_container.append(msg["message"])

    return 'New message successfully added', 201

@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(debug=True)