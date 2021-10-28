import concurrent.futures
import requests
import os

SECONDARY_FRST = os.getenv('SECONDARY_FRST_BASE_PATH', 'http://localhost:5001')
SECONDARY_SCND = os.getenv('SECONDARY_SCND_BASE_PATH', 'http://localhost:5002')


class MultiThreadProcessing:

    def __init__(self):
        self.endpoints = [SECONDARY_FRST + '/messages', SECONDARY_SCND + '/messages']
        print(self.endpoints)

    def replicate_message(self, msg, w):
        ack_count = 0

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.endpoints))
        results = list(map(lambda endpoint: executor.submit(requests.post, endpoint, json=msg), self.endpoints))
        if w != 0:
            for future in concurrent.futures.as_completed(results):
                if future.result():
                    ack_count += 1
                    if ack_count == w:
                        return ack_count

        return ack_count
