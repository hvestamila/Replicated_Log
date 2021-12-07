import concurrent.futures
import requests
import os
import time
from exceptions import HealthError


SECONDARY_FRST = os.getenv('SECONDARY_FRST_BASE_PATH', 'http://localhost:5001')
SECONDARY_SCND = os.getenv('SECONDARY_SCND_BASE_PATH', 'http://localhost:5002')

executor = concurrent.futures.ThreadPoolExecutor()

class MultiThreadProcessing:

    def __init__(self):
        self.endpoints = [SECONDARY_FRST, SECONDARY_SCND ]
        self.health = {SECONDARY_FRST: 'suspected',
                    SECONDARY_SCND: 'suspected'}

    def isQuorum(self):
        totalHealty = 0
        for url in self.endpoints:
            if self.health.get(url) == 'healthy':
                totalHealty += 1

        return (int(len(self.endpoints) / 2)) <= totalHealty

    def deliver_message(self, url, json, logger):
        try:
            if self.health.get(url) == 'healthy':
                response = requests.post(url=url + '/messages', json=json, timeout=12)
            else:
                logger.error(f"Health of {url} is {self.health.get(url)}")
                return False
        except Exception as err:
            logger.error(f'URL: {url}; Exception: {repr(err)}')
            return False
        logger.info(f'URL: {url}; Response code: {response.status_code}')
        return response.ok

    def send_post(self, url_secondary, message, logger):
        delay_time = 1
        while not self.deliver_message(url=url_secondary, json=message, logger=logger):
            logger.info(f'Host is unreachable: {url_secondary}; Waiting for {delay_time} seconds')
            time.sleep(delay_time)
            if delay_time < 8:
                delay_time = delay_time * 2
        return True

    def replicate_message(self, msg_id, msg, w, logger):
        ack_count = 0
        msg["msg_id"] = msg_id

        results = list(
            map(lambda endpoint: executor.submit(self.send_post, url_secondary=endpoint,
                                                 message=msg, logger=logger), self.endpoints))
        if w != 0:
            for future in concurrent.futures.as_completed(results):
                result = future.result()
                if result:
                    ack_count += 1
                    if ack_count == w:
                        return ack_count

        return ack_count

    def health_setter(self, endpoint, status, logger):
        if not self.health.get(endpoint) == status:
            self.health.update({endpoint:status})
            logger.info(f'{self.health}')


    def health_getter(self, endpoint):
        try:
            return requests.get(endpoint+'/health', timeout=2).ok
        except:
            return False


    def health_process(self, logger, endpoint):
        bad_requests_count = 6
        while True:
            if self.health_getter(endpoint=endpoint):
                if bad_requests_count > 0:
                    bad_requests_count -= 1
            else:
                if bad_requests_count < 12:
                    bad_requests_count += 1

            if bad_requests_count >= 12:
                self.health_setter(endpoint, 'unhealthy', logger)
            elif bad_requests_count >= 6:
                self.health_setter(endpoint, 'suspected', logger)
            else:
                self.health_setter(endpoint, 'healthy', logger)
            time.sleep(1)

    def runHeardbeat(self, logger):
        for url in self.endpoints:
            executor.submit(self.health_process,
                            endpoint=url,
                            logger=logger)