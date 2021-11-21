class MessageContainer:

    def __init__(self):
        self.messages = dict()

    def append(self, key, msg):
        self.messages[key] = msg

    def get_all(self):
        if len(self.messages) == 0 or min(self.messages.keys()) != 1:
            return {}
        if len(self.messages) == max(self.messages.keys()):
            return self.messages

        for key in self.messages.keys():
            next_key = key+1
            if next_key not in self.messages.keys():
                return {key: value for key, value in self.messages.items() if key < next_key}
