import socket

from client import Client

LISTEN_AMOUNT = 5
SERVER_TIMEOUT = 0.5

class Server(object):
    def __init__(self, ip, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(SERVER_TIMEOUT)

        self._socket.bind((ip, port))
        self._socket.listen(LISTEN_AMOUNT)

        self._clients = []

        print '[+] created the server successfully'

    def start(self):
        try:
            self._run()
        except KeyboardInterrupt:
            pass
        finally:
            self._close()
            print '[*] bye bye!'

    def _run(self):
        while True:
            try:
                client_sock, client_addr = self._socket.accept()

                client = Client(client_sock, self._clients, *client_addr)
                client.start()

                self._clients.append(client)
            except socket.timeout:
                continue
            except Exception as e:
                print '[-] unknown exception:', e
                break

    def _close(self):
        for client in self._clients:
            client.close()
            client.join()
        
        self._socket.close()
