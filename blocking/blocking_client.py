# -*- coding: utf-8 -*-

import socket

s = socket.socket()

s.connect(('127.0.0.1', 9090))

while True:
    input_msg = input('input>>> ')
    if input_msg == '0':
        s.sendall(input_msg.encode())
        msg = s.recv(1024)
        print(msg.decode())
        s.close()
        break
    s.sendall(input_msg.encode())
    msg = s.recv(1024)
    print(msg.decode())
