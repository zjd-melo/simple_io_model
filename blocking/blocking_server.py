# -*- coding: utf-8 -*-

"""
同步阻塞I/O, 一次只允许一个连接, 阻塞于recv()
响应快,延迟低,用多线程或者多进程可以处理多个请求适用于连接数量少的场景
"""

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('127.0.0.1', 9090))

s.listen(2)  # 单线程下设置backlog没有什么意义, 因为一次只能处理一个请求

print("server is running...")

while True:
    # 一次只能处理一个请求
    conn, address = s.accept()  # conn socket对象 address是client端的地址
    print(conn)
    # socket.socket fd=232, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0,
    # laddr=('127.0.0.1', 56974), raddr=('127.0.0.1', 9090)>
    while True:
        data = conn.recv(1024)
        if data.decode() == '0':
            conn.sendall(b'goodby')
            print("connection closed by server. ", "client is: {}:{}".format(*address))
            conn.close()
            break
        print("message from " + address[0] + ":" + str(address[1]) + "--> " + data.decode())
        conn.sendall(b"server say: " + data)
