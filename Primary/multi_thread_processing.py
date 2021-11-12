import concurrent.futures
import requests
import os
import time

SECONDARY_FRST = os.getenv('SECONDARY_FRST_BASE_PATH', 'http://localhost:5001')
SECONDARY_SCND = os.getenv('SECONDARY_SCND_BASE_PATH', 'http://localhost:5002')

class MultiThreadProcessing:

    def __init__(self):
        self.endpoints = [SECONDARY_FRST + '/messages', SECONDARY_SCND + '/messages']
        print(self.endpoints)
    def DeliveryMessage(self, url, json):
        try:
            response = requests.post(url=url, json=json)
        except:
            print('URL: ', url)
            print('Exception appear')
            return False
        print('URL: ', url)
        print('Responce code ', response.status_code )
        return response.ok

    def SendPost(self, url_secondary, message):
        dellay_time = 1;
        while  (self.DeliveryMessage(url=url_secondary, json=message) != True):
            print('Host is unreachable should wait ', dellay_time, 'seconds')
            time.sleep(dellay_time)
            dellay_time = dellay_time * 2
        return True

    def replicate_message(self, msg_id, msg, w):
        ack_count = 0
        msg["msg_id"] = msg_id

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(self.endpoints))

        results = list(map(lambda endpoint: executor.submit(self.SendPost, url_secondary=endpoint, message=msg), self.endpoints))
        if w != 0:
            for future in concurrent.futures.as_completed(results):
                result = future.result()
                if result == True:
                    ack_count += 1
                    if ack_count == w:
                        return ack_count

        return ack_count
