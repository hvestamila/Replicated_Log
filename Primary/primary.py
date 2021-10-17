from flask import Flask, request
from message_container import MessageContainer
from multi_thread_processing import MultiThreadProcessing

app = Flask(__name__)

msg_container = MessageContainer()

multi_threaded_process = MultiThreadProcessing()


@app.route('/health')
def index():
    return "OK"


@app.route('/messages', methods=['POST'])
def save_msg():
    msg = request.get_json()
    res = multi_threaded_process.replicate_message(msg)

    if res == len(multi_threaded_process.endpoints):
        msg_container.append(msg["message"])

    return 'New message successfully added', 201


@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
