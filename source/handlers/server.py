import socket

LISTEN_AMOUNT = 5
TIMEOUT = 1

class Server(object):
    def __init__(self, ip, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.settimeout(TIMEOUT)

        self._socket.bind((ip, port))
        self._socket.listen(LISTEN_AMOUNT)

        self._clients = []

        print '[+] created the server successfully'

    def start(self):
        self.run()

    def run(self):
        while True:
            try:
                client_sock, client_addr = self._socket.accept()
                client = Client(client_sock, *client_addr)

                self._clients.append(client)
            except socket.timeout:
                continue
            except:
                print '[-] unknown exception'
                break

        for client in self._clients:
            client.close()
        
        self._socket.close()
