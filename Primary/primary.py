from flask import Flask, request
from message_container import MessageContainer
from multi_thread_processing import MultiThreadProcessing
# from uuid import uuid4

app = Flask(__name__)

msg_container = MessageContainer()

multi_threaded_process = MultiThreadProcessing()
g_uid = 0

def get_next_uid():
    global g_uid
    g_uid = g_uid + 1
    return g_uid


@app.route('/health')
def index():
    return "OK"


@app.route('/messages', methods=['POST'])
def save_msg():
    income_msg = request.get_json()

    msg = dict()
    try:
        msg["message"] = income_msg["message"]
    except:
        return 'The field "message"  was not found in JSON', 400
    try:
        write_concern = int(income_msg["write_concern"]) - 1
    except:
        write_concern = len(multi_threaded_process.endpoints)
        print("Missing write_concern parameter in JSON")

    msg_id = get_next_uid()

    if write_concern > len(multi_threaded_process.endpoints):
        write_concern = len(multi_threaded_process.endpoints)
    elif write_concern < 0:
        write_concern = 0
    msg_container.append(msg_id, msg["message"])

    writes_successfully = multi_threaded_process.replicate_message(msg_id, msg, write_concern)

    print(writes_successfully, write_concern)

    return 'New message successfully added', 201

@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
