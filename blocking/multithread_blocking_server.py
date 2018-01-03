# -*- coding: utf-8 -*-

import socket
import threading


def run(sock, addr):
    while True:
        data = sock.recv(1024)
        if data.decode() == '0':
            sock.sendall(b"goodby")
            print("connection closed. ", "client is: {}:{}".format(*address))
            print(threading.current_thread().getName() + " quit")
            sock.close()
            break
        print(threading.current_thread().getName())
        print("message from {}:{}".format(*addr) + " --> " + data.decode())
        sock.sendall(b"server say: " + data)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 9090))

s.listen(5)

print("server is running...")

while True:
    try:
        # 有请求过来, 开启一个线程处理
        conn, address = s.accept()
        t = threading.Thread(target=run, args=(conn, address))
        t.start()
        print("current thread count: " + str(threading.active_count()))
    except Exception as e:
        print(e)
        break
