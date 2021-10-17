import concurrent.futures
import requests
import os


SECONDARY_FRST = os.getenv('SECONDARY_FRST_BASE_PATH', 'http://localhost:5001')
SECONDARY_SCND = os.getenv('SECONDARY_SCND_BASE_PATH', 'http://localhost:5002')


class MultiThreadProcessing:

    def __init__(self):
        self.endpoints = [SECONDARY_FRST+'/messages', SECONDARY_SCND+'/messages']
        print(self.endpoints)

    def replicate_message(self, msg):
        replicate_count = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.endpoints)) as executor:
            results = executor.map(lambda endpoint: requests.post(endpoint, json=msg), self.endpoints)
            for result in results:
                if result.ok:
                    replicate_count += 1

        return replicate_count
