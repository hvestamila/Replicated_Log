import json


class MessageContainer:

    def __init__(self):
        self.msg_container = dict()

    def append(self, key, msg):
        self.msg_container[key] = msg

    def get_all(self):

        # TO DO:
        # fix encoding because GET doesn't work after POST
        return json.dumps(list(self.msg_container.values())).encode("utf-8")
