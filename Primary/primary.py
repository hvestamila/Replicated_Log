from http.server import HTTPServer, BaseHTTPRequestHandler
from message_container import MessageContainer


class HttpServer:
    def __init__(self):
        self.msg_container = MessageContainer()

        # FOR TESTING PURPOSES 1 MESSAGE IS ADDED TO DICT
        self.msg_container.append('1', 'Message 1 Test')
        server = HTTPServer(('localhost', 8000), lambda *args: SimpleHTTPRequestHandler(self.msg_container, *args))
        server.serve_forever()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, msg_container, *args):
        self.msg_container = msg_container
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # RETURN ALL MESSAGES IN MESSAGE CONTAINER:
        self.wfile.write(self.msg_container.get_all())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # Next, we need to
        # 1. Send a new message to Secondary 1 and Secondary 2
        # 2. Receive ACK that response_code = 200 for Secondary 1 and Secondary 2
        # 3. Then append(msg) to dict

        # for now, only append() will work because there is no Secondary created yet
        self.msg_container.append(len(self.msg_container.msg_container.keys())+1, body)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(body)

        # This print is to test if the new message appended to dict
        print(self.msg_container)

class main:
    def __init__(self):
        self.server = HttpServer()

if __name__ == '__main__':
    m = main()
