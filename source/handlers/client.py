import socket
import json
from threading import Thread, Lock


from ..common import Request, Responses
from ..controllers import get_controller_func
from ..games import find_game


BUFFER_SIZE = 1024
CLIENT_TIMEOUT = 0.5


class Client(Thread):
    def __init__(self, sock, clients, ip, port):
        super(Client, self).__init__()

        self._socket = sock
        self._socket.settimeout(CLIENT_TIMEOUT)
        self._in_game = False
        self._game_id = -1
        self._player_name = ''
        self._clients = clients
        self._ip = ip
        self._port = port
        self._running = True
        self._socket_lock = Lock()

        self._error_occurred = False

        print '[*] %s:%d has connected to the server' % (ip, port)

    def run(self):
        while self._running:
            try:
                request = Request.deserialize(self._recieve_request())
                self.handle_request(request.code, request.args)
            except ValueError:
                self._send_bad_request()
            except socket.timeout:
                continue
            except socket.error:
                self._error_occurred = True
                return self.close()
            except Exception as e:
                print '[-]', e
                self._error_occurred = True
                return self.close()

    def handle_request(self, code, args):
        controller_function = get_controller_func(code)
        response = controller_function(args, self)
        self._send_message(response.serialize())

    def close(self):
        if self._in_game:
            game = find_game(self._game_id)
            game.player_disconnected(self._player_name)

        if self._error_occurred:
            self._clients.remove(self)

        self._running = False

        with self._socket_lock:
            self._socket.close()

        print '[*] %s:%d has disconnected from the server' % (
            self._ip, self._port)

    def _recieve_request(self):
        with self._socket_lock:
            buffer = self._socket.recv(BUFFER_SIZE)
            if not buffer:
                raise socket.error()

            if len(buffer) == BUFFER_SIZE:
                while True:
                    try:
                        buffer += self._socket.recv(BUFFER_SIZE)
                    except Exception:
                        break

            request = json.loads(buffer)

            return request

    def _send_message(self, message):
        self._socket.send(message)

    def _send_bad_request(self):
        with self._socket_lock:
            self._send_message(Responses.BAD_REQUEST.serialize())
