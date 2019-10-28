#!/usr/bin/env python3

import os
import redis
import socket
import json

def sendMsg(conn,message):
    conn.sendall(message.encode('utf-8'))

def sendData(conn,message,data):
    conn.sendall(message.encode('utf-8')+data)

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('',65432))
    s.listen(1)
    conn, addr = s.accept()
    cache = redis.Redis(host='localhost',port=6379)
    cache.ping()
    print('connected:',addr)
    while True:
        data = conn.recv(1024)
        response = None
        try:
            request = json.loads(data)
            action = request["action"]
            key = request["key"]
        except:
            response = {"status":"Bad Request"}
            sendMsg(conn, json.dumps(response))
            continue

        try: 
            if (action  == "put"):
                if cache.exists(key):
                    response = {"status":"Ok"}
                else:
                    cache.set(key,json.dumps(request["message"]))
                    response = {"status":"Created"}
            elif (action  == "get"):
                if cache.exists(key):
                    response = {"status":"Ok", "message": json.loads(cache.get(key))}
                else:
                    response = {"status":"Not found"}
            elif (action  == "delete"):
                if cache.exists(key):
                    existing = cache.get(key)
                    cache.delete(key)
                    response = {"status":"Ok", "message": json.loads(existing)}
                else:
                    response = {"status":"Not found"}         
            sendMsg(conn, json.dumps(response))
        except:
            response = {"status":"Internal Server Error"}
            sendMsg(conn, json.dumps(response))
            continue
        