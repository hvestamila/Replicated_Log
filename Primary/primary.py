from flask import Flask, request
from message_container import MessageContainer
from multi_thread_processing import MultiThreadProcessing
# from uuid import uuid4
import sys
sys.stdout.flush()

app = Flask(__name__)

msg_container = MessageContainer()

multi_threaded_process = MultiThreadProcessing()


@app.route('/health')
def index():
    return "OK"


@app.route('/messages', methods=['POST'])
def save_msg():
    msg = request.get_json()
    write_concern = int(request.args.get('w', default=1)) - 1   # total number - primary = number of secondaries
    msg_id = msg_container.length() + 1

    if write_concern > len(multi_threaded_process.endpoints):
        write_concern = len(multi_threaded_process.endpoints)
    elif write_concern < 0:
        write_concern = 0

    writes_successfully = multi_threaded_process.replicate_message(msg_id, msg, write_concern)

    msg_container.append(msg_id, msg["message"])
    print(writes_successfully, write_concern)

    return 'New message successfully added', 201

@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
