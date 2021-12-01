class HealthError(Exception):
    """Base class for Health exception"""
    def __init__(self, endpoint, status):
        self.endpoint = endpoint
        self.message = f"Health of {endpoint} is {status}"
        super().__init__(self.message)
