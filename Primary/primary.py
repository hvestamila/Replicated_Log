from flask import Flask, request
from message_container import MessageContainer
from multi_thread_processing import MultiThreadProcessing
import json
import os
from celery_tasks import make_celery


# from uuid import uuid4

app = Flask(__name__)
msg_container = MessageContainer()
multi_threaded_process = MultiThreadProcessing()
g_uid = 0
celery = make_celery(app)

# t2 = health_tick(url='http://localhost:5002/health',logger=app.logger)


@celery.task()
def health_tick(self, url, logger):
    while True:
        try:
            status = requests.get(url=url).status_code
        except Exception:
            status = 400

        logger.info(f'--------{status}----------')
        time.sleep(2)


def get_next_uid():
    global g_uid
    g_uid = g_uid + 1
    return g_uid


@app.route('/health')
def index():
    return "OK"


@app.route('/messages', methods=['POST'])
def save_msg():
    # income_msg = request.get_json()
    income_msg = request.get_data()
    income_msg = json.loads(income_msg)

    msg = dict()
    try:
        msg["message"] = income_msg["message"]
    except:
        app.logger.error(f'The field "message" was not found in JSON')
        return 'The field "message" was not found in JSON', 400

    try:
        write_concern = int(income_msg["write_concern"]) - 1

    except:
        write_concern = len(multi_threaded_process.endpoints)
        app.logger.info(f'Missing write_concern parameter in JSON. Replaced with {write_concern}')

    msg_id = get_next_uid()

    if write_concern > len(multi_threaded_process.endpoints):
        write_concern = len(multi_threaded_process.endpoints)
    elif write_concern < 0:
        write_concern = 0
    msg_container.append(msg_id, msg["message"])

    writes_successfully = multi_threaded_process.replicate_message(msg_id, msg, write_concern, app.logger)

    app.logger.info(f'Number of successful writes to secondary: {writes_successfully}. Write concern: {write_concern + 1}')

    return 'New message successfully added', 201


@app.route('/messages', methods=['GET'])
def return_msg():
    return msg_container.get_all(), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    url_1 = 'http://localhost:5001/health'
    r = health_tick.delay(url=url_1,logger=app.logger)
    x = send_mail.apply_async(args=[url_1, app.logger])
    app.logger.info(f'Print----------- {x}')
