#!/usr/bin/python3
#Chat client with TLS

import socket, sys, threading, ssl, pprint

PORT = 9999

class ChatClient(threading.Thread):

    def __init__(self, port, host='localhost'):
        threading.Thread.__init__(self)
        self.running = True
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #self.socket.connect((self.host, port))
        self.ssl_sock = ssl.wrap_socket(self.socket,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)

        self.ssl_sock.connect((self.host, port))
        print(repr(self.ssl_sock.getpeername()))
        print(self.ssl_sock.cipher())
        print(pprint.pformat(self.ssl_sock.getpeercert()))


    def send_message(self, msg):
        # Encrypt chat messages in this method
        data = bytes(msg, 'utf-8')
        #self.socket.send(data)
        self.ssl_sock.write(data)

    def ReceiveMessage(self):
        # Decrypt chat messages in this method
        while(True):
            #data = self.socket.recv(1024)
            data = self.ssl_sock.read(1024)
            if data:
                msg = data.decode('utf-8')
                if(msg[:5]=='.exit'):
                    self.running=False
                    return
                print(msg)

    def run(self):
        print("Starting Client")

        self.username = input("Username: ")
        print(".exit to quit")
        data = bytes(self.username, 'utf-8')
        #self.socket.send(data)
        self.ssl_sock.write(data)
        
        threading.Thread(target=self.ReceiveMessage).start()
        
        while(self.running):
            msg = input()
            self.send_message(msg)

        sys.exit()
        
if __name__ == '__main__':
    client = ChatClient(PORT)
    client.start()
