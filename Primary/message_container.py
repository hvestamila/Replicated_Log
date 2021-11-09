class MessageContainer:

    def __init__(self):
        self.messages = dict()

    def append(self, key, msg):
        self.messages[key] = msg

    def length(self):
        return len(self.messages.keys())

    def get_all(self):
        return self.messages
