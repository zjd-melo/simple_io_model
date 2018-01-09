# -*- coding: utf-8 -*-

import socket

flag = 1

s = socket.socket()

s.connect(('127.0.0.1', 9090))

while flag:
    input_msg = input('input>>> ')
    if input_msg == '0':
        break
    s.sendall(str(input_msg).encode())
    msg = s.recv(1024)
    print(msg)
s.close()
