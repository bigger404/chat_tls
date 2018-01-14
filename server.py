#!/usr/bin/python3

#Chat server with TLS

# Setup the key and certificate:
# openssl genrsa -des3 -out server.orig.key 2048
# openssl rsa -in server.orig.key -out server.key
# openssl req -new -key server.key -out server.csr
# openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

import socket, sys, threading, ssl

class YackServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.MAX_Threads = 25
        self.port = 9999
        self.host = 'localhost'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}

        try:
            self.server.bind((self.host, self.port))
        except socket.error:
            print('Socket Error %s' % (socket.error))
            sys.exit()

        self.server.listen(self.MAX_Threads)

    def broadcast (self, username, msg):
        for user in self.users:
            if (user is not username):
                try:
                    self.users[user].write(bytes(username+": "+msg,'utf-8'))
                except:
                    enc_stream.close()
                    if enc_stream in self.users:
                        self.users.remove(enc_stream)

    def run_thread(self, username, enc_stream, addr):
        print('Client connected with ' + addr[0] + ':' + str(addr[1]))
        while True:
            try:
                data = enc_stream.read(1024)
                msg = data.decode('utf-8')
                #print("debug")
                #print(msg)
                if (msg[:5] == ".exit"):
                    self.broadcast("User "+username+" has quit.")
                    print("User "+username+" has quit.")
                    self.users[username].write(bytes(".exit",'utf-8'))
                    self.users.remove(username)
                    enc_stream.close()
                    return
                self.broadcast(username, data.decode('utf-8'))
                print(username + ": " + data.decode('utf-8')) 
            except:
                self.broadcast(username, username+"(%s, %s) is offline\n" % addr)
                enc_stream.close()
                del self.users[username]
                return

    def run(self):
        print('Listening on port %s' % (self.port))
        while True:
            conn, addr = self.server.accept()
            enc_stream = ssl.wrap_socket(conn,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key")
            data = enc_stream.read(1024)
            username = data.decode('utf-8')
            if (username not in self.users):
                self.users[username] = enc_stream
                print(username, "connected")
                threading.Thread(target=self.run_thread, args=(username, enc_stream, addr)).start()
            else:
                enc_stream.write(bytes(username+" not available. Please try again.",'utf-8'))
                enc_stream.close()


if __name__ == '__main__':

    server = YackServer()
    server.run()
