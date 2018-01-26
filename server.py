#!/usr/bin/python3
#Chat server with TLS

# Setup the key and certificate:
# openssl genrsa -des3 -out server.orig.key 2048
# openssl rsa -in server.orig.key -out server.key
# openssl req -new -key server.key -out server.csr
# openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

import socket, sys, threading, ssl, os, datetime

class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.MAX_Threads = 25
        self.port = int(port)
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Socket Error %s' % (socket.error))
            sys.exit()

        self.server.listen(self.MAX_Threads)

    def broadcast (self, username, msg):
        if msg==".exit":
            self.users[username].write(bytes(msg, 'utf-8'))
        for user in self.users:
            if (user is not username):
                try:
                    self.users[user].write(bytes(username+": "+msg,'utf-8'))
                except:
                    enc_stream.close()
                    if enc_stream in self.users:
                        self.users.remove(enc_stream)

    def run_thread(self, username, enc_stream, addr):
        print(str(datetime.datetime.now()).split('.')[0] + ' '+ username + ' connected from ' + addr[0] + ':' + str(addr[1]))
        while True:
            try:
                data = enc_stream.read(1024)
                msg = data.decode('utf-8')
                self.broadcast(username, data.decode('utf-8'))
                print(username + ": " + data.decode('utf-8')) 
            except:
                self.broadcast(username, username+"(%s, %s) has quit!\n" % addr)
                enc_stream.close()
                self.users.pop(username)                
                return

    def run(self):
        print('Listening on port %s' % (self.port))
        while True:
            try:
                conn, addr = self.server.accept()
                enc_stream = ssl.wrap_socket(conn, server_side=True, certfile="server.crt", keyfile="server.key")
                data = enc_stream.read(1024)
                username = data.decode('utf-8')
                if (username not in self.users and username != '.exit'):
                    self.users[username] = enc_stream
                    #print(username, "connected")
                    threading.Thread(target=self.run_thread, args=(username, enc_stream, addr)).start()
                else:
                    enc_stream.write(bytes(username+" not available. Please try again.",'utf-8'))
                    enc_stream.close()
            except Exception as e:
                print('Error %s' % (e))

if __name__ == '__main__':
    host = 'localhost'
    port = '9999'
    os.system('clear')
    server = Server(host,port)
    server.run()
