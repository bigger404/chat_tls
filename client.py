#!/usr/bin/python3
#Chat client with TLS

import socket, sys, threading, ssl, pprint, os

class ChatClient(threading.Thread):

    def __init__(self, host,port):
        threading.Thread.__init__(self)
        self.username = ''
        self.running = True
        self.host = host
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssl_sock = ssl.wrap_socket(self.socket, ca_certs="server.crt", cert_reqs=ssl.CERT_REQUIRED)
        #self.ssl_sock = ssl.wrap_socket(self.socket, ca_certs="bad_server.crt", cert_reqs=ssl.CERT_REQUIRED)
        self.ssl_sock.connect((self.host, self.port))
        print(repr(self.ssl_sock.getpeername()))
        print(self.ssl_sock.cipher())
        print(pprint.pformat(self.ssl_sock.getpeercert()))
            
    def send_message(self, msg):
        data = bytes(msg, 'utf-8')
        self.ssl_sock.write(data)

    def ReceiveMessage(self):
        while(self.running):
            try:
                data = self.ssl_sock.read(1024)
                if data:
                    msg = data.decode('utf-8')
                    if msg.find('.exit') == -1: print(msg)
            except:
                return

    def run(self):
        if(self.running):
            print("Server Certificate OK")
            while self.username == '':
                self.username = input("Username: ")
            print(".exit to quit")
            data = bytes(self.username, 'utf-8')
            self.ssl_sock.write(data)
            threading.Thread(target=self.ReceiveMessage).start()        

        while(self.running):
            msg = input()
            if len(msg)>0:
                if msg == '.exit':
                    self.running=False
                self.send_message(msg)
        
        print("Closing connection")
        self.ssl_sock.close()
        sys.exit()
        
if __name__ == '__main__':
    #host = 'localhost'
    #port = '9999'
    host = input('Server hostname: (localhost)')
    port = input('Server port: (9999)')
    if host == '': host = 'localhost'
    if port == '': port = '9999'
    os.system('clear')
    client = ChatClient(host,port)
    client.start()
