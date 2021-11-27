def health_run(endpoint, logger):
    global statuses
    bad_requests_count = 0
    while True:
        try:
            status = requests.get(url=endpoint+'/health').status_code
            bad_requests_count = 0
        except Exception:
            bad_requests_count += 1
            status = 400
        if bad_requests_count >= 12:
            statuses.update({endpoint:'unhealthy'})
        elif bad_requests_count >= 6:
            statuses.update({endpoint:'suspected'})
        if bad_requests_count < 6:
            statuses.update({endpoint:'healthy'})

        logger.info(f'----{endpoint}:{statuses}----')
        time.sleep(3)
