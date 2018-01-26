# chat_tls
Basic chat server with TLS
python3 with barebones tls

To setup the certificate and server key:

 #openssl genrsa -des3 -out server.orig.key 2048
 #openssl rsa -in server.orig.key -out server.key
 #openssl req -new -key server.key -out server.csr
 #openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

To use:
Setup a server.crt and server.key
Edit the server.py host and port values. host = 'localhost' will only work for testing on the same computer.
The server needs the server.key and server.crt files in the same dir. The client needs the server.crt file in the same directory. Launch server.py, then start client.py
