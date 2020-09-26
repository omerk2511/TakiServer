import socket
import json
from threading import Thread, Lock

from ..requests.utils import validate_request


BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 0.5

# move to responses/
BAD_REQUEST = {
    "status": "bad_request",
    "args": {
        "message": "Bad request"
    }
}

CREATE_GAME = {
    "status": "success",
    "args": {
        "game_id":  "",
        "jwt":      ""
    }
}


class Response(object): 
    def __init__(self, status, **kwargs): #each response has status and args
        self.status = status
        self.args = kwargs

    def serialize(self):
        return json.dumps(
            {
                "status": self.status,
                "args": self.args
            }
        )


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

        self.request_handler = {
            "create_game" : self.create_game
        }

        print '[*] %s:%d has connected to the server' % (ip, port)

    def run(self):
        while self._running:
            try:
                request = self._recieve_request()
                self.handle_request(request)
            except ValueError:
                self._send_bad_request()
            except socket.timeout:
                continue
            except socket.error:
                return self.close()

    def handle_request(self, request):
        code = request['code']
        args = request['args']
        response = self.request_handler[code](**args)
        self._socket.send(response)


    def create_game(self, **kwargs):
        lobby_name = kwargs.get('lobby_name')
        player_name  =kwargs.get('player_name')
        password = kwargs.get('password').strip()
        if not password.strip(): password = None # if password field is empty
        print '[*] %s created lobby %s' % (player_name,lobby_name)
        game_id = '1' # random 
        token = 'abcd' # jwt
        response = Response(status = 'success', game_id = game_id, jwt = token)
        return response.serialize()


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

    def _send_bad_request(self):
        with self._socket_lock:
            self._socket.send(json.dumps(BAD_REQUEST))
