from handlers import Server

IP = '0.0.0.0'
PORT = 8080

def main():
    server = Server(IP, PORT)
    server.start()

if __name__ == '__main__':
    main()
