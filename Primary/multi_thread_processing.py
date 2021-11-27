import concurrent.futures
import requests
import os
import time


SECONDARY_FRST = os.getenv('SECONDARY_FRST_BASE_PATH', 'http://localhost:5001')
SECONDARY_SCND = os.getenv('SECONDARY_SCND_BASE_PATH', 'http://localhost:5002')

executor = concurrent.futures.ThreadPoolExecutor()


class MultiThreadProcessing:

    def __init__(self):
        self.endpoints = [SECONDARY_FRST + '/messages', SECONDARY_SCND + '/messages']
        self.health = {SECONDARY_FRST:'unhealthy',
                    SECONDARY_SCND:'unhealthy'}

    def deliver_message(self, url, json, logger):
        try:
            response = requests.post(url=url, json=json)
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
        return requests.get(endpoint+'/health').status_code


    def health_process(self, logger, endpoint):
        bad_requests_count = 0
        while True:
            try:
                status = self.health_getter(endpoint=endpoint)
                bad_requests_count = 0
            except Exception:
                bad_requests_count += 1
                status = 400
            if bad_requests_count >= 12:
                self.health_setter(endpoint, 'unhealthy', logger)
            elif bad_requests_count >= 6:
                self.health_setter(endpoint, 'suspected', logger)
            elif bad_requests_count < 6:
                self.health_setter(endpoint, 'healthy', logger)
            time.sleep(1)
