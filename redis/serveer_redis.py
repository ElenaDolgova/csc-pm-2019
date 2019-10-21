#!/usr/bin/env python3

import os
import redis
import socket

def cashed(data):
    cache = redis.Redis(host='redisserver',port=6379)
    cache.ping()
    if cache.exists(data):
        return True
    else:
        cache.set(data,data)
        return False

def sendMsg(conn,message):
    conn.sendall(message.encode('utf-8'))

def sendData(conn,message,data):
    conn.sendall(message.encode('utf-8')+data)

s = socket.socket()
s.bind(('',65432))
s.listen(1)
conn, addr = s.accept()
print('connected:',addr)

while True:
    data = conn.recv(1024)
    # if not data:
    #     print("Got:",data)
    #     sendMsg(conn,"Bye")
    #     break
    if cashed(data):
        sendData(conn,"Cached:",data)
    else:
        conn.sendall("OK:".encode('utf-8')+data)
