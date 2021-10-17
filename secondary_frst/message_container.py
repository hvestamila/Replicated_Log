class MessageContainer:

    def __init__(self):
        self.messages = dict()

    def update(self, key, msg):
        self.messages[key] = msg

    def append(self, msg):
        self.update(len(self.messages.keys()) + 1, msg)

    def get_all(self):
        return self.messages
