# -*- coding: utf-8 -*-

"""
select I/O复用 读写分离
接收一个连接, 放入可读列表, 如果client发送数据, select返回可读socket, 读取数据, 把该socket放入可写列表, select返回可写列表把数据写回给client
接下来select返回可写列表, 发现没有数据要写给client, 把该socket从可写列表移除
"""

import socket
import select
import queue

# 创建监听套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setblocking(False)

print("starting up on 127.0.0.1:9090")

server_socket.bind(('127.0.0.1', 9090))

server_socket.listen()

# 可读socket
read_list = [server_socket]
# 可写socket
write_list = []

messahe_queues = {}

while read_list:
    # select可以操作的socket
    print("selecting...")
    readable, writeable, exception = select.select(read_list, write_list, read_list)
    
    print('*' * 500)
    print("current readable, writeable, exception", readable, writeable, exception)
    print('*' * 500)
    
    # 处理可读的socket(recv)
    for sock in readable:
        if sock is server_socket:
            # server_socket可读说明有新的连接
            conn, client_addr = sock.accept()
            print("new connection from {}:{}".format(*client_addr))
            conn.setblocking(False)  # **** 如果不设置就是同步阻塞了, select是同步非阻塞的(内核帮线程轮询, 复用线程)
            read_list.append(conn)  # 把新的连接放入可读列表,让select轮询
            messahe_queues[conn] = queue.Queue()  # 每个连接都有一个queue, 存放发送的数据
        else:
            # 有可读的socket
            data = sock.recv(1024)
            if data:
                # 可读socket有数据
                print("received data from {}:{}".format(*sock.getpeername()))
                messahe_queues[sock].put(data)
                # 加入可写列表轮询
                if sock not in write_list:
                    write_list.append(sock)
            else:
                # 没有数据, 断开连接
                print("{}:{} client closed".format(*sock.getpeername()))
                # 把这个连接从轮询数组中移除
                if sock in write_list:
                    write_list.remove(sock)
                read_list.remove(sock)
                sock.close()
                # 删除该连接对应的queue
                del messahe_queues[sock]
    
    # 处理可写的socket(send)
    for sock in writeable:
        try:
            reply = messahe_queues[sock].get_nowait()
        except queue.Empty:
            # 连接对应的queue中没有数据, 即没有数据发给client, 从可写列表中移除
            print("no reply to {}:{} client".format(*sock.getpeername()))
            write_list.remove(sock)
        else:
            print('reply {} to {}:{} client'.format(reply, *sock.getpeername()))
            sock.send(reply)
    
    # 处理异常
    for sock in exception:
        print("handle exception for {}:{} client".format(*sock.getpeername()))
        # 停止轮询异常连接
        read_list.remove(sock)
        if sock in write_list:
            write_list.remove(sock)
        sock.close()
        
        del messahe_queues[sock]
