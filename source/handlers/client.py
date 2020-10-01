import socket
import json
from threading import Thread, Lock


from ..common import Message, Request, Response
from ..requests.utils import validate_request
from ..controllers import *


BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 0.5 

# move to responses/
BAD_REQUEST = {
    "status": "bad_request",
    "args": {
        "message": "Bad request"
    }
}




class Client(Thread):
    def __init__(self, sock, clients, ip, port):
        super(Client, self).__init__()

        self._socket = sock
        self._socket.settimeout(CLIENT_TIMEOUT)

        self._clients = clients
        self._ip = ip
        self._port = port
        self._running = True
        self._socket_lock = Lock()
        print '[*] %s:%d has connected to the server' % (ip, port)

    def run(self):
        while self._running:
            try:
                request = self._recieve_request()
                request = Request.deserialize(request)
                self.handle_request(request)

            except ValueError:
                self._send_bad_request()
            except socket.timeout:
                continue
            except socket.error:
                return self.close()


    def handle_request(self, request):
        try:
            code = request.code
            args = request.args
            controller_function = get_controller_func(code)
            
            if controller_function:
                response = get_controller_func(code)(args)
                self._send_message(response.serialize())
            else:
                self._send_bad_request()
        except Exception as e:
            print ('[EXCEPTION]',e)
            self._send_bad_request()


    def close(self):
        self._clients.remove(self)
        self._running = False

        with self._socket_lock:
            self._socket.close()

        print '[*] %s:%d has disconnected from the server' % (self._ip, self._port)


    def _recieve_request(self):
        with self._socket_lock:
            buffer = self._socket.recv(BUFFER_SIZE)
            if not buffer: raise socket.error()

            if len(buffer) == BUFFER_SIZE:
                while True:
                    try:
                        buffer += self._socket.recv(BUFFER_SIZE)
                    except:
                        break

            request = json.loads(buffer)
            validate_request(request)

            return request


    def _send_message(self,message):
        self._socket.send(message)

    def _send_bad_request(self):
        with self._socket_lock:
            self._socket.send(json.dumps(BAD_REQUEST))
