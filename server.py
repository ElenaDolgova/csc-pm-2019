#!/usr/bin/env python3
import socket

s = socket.socket()
s.bind(('',65432))
s.listen(1)
conn, addr = s.accept()
print('connected:',addr)
logFile = open("server.log","w")
while True:
    data = conn.recv(1024)
    logFile.write(data)
    conn.sendall("OK:".encode('utf-8')+data)

logFile.close()
conn.close()