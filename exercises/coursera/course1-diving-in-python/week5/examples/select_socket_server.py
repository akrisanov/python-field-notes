import select
import socket

sock = socket.socket()
sock.bind(("127.0.0.1", 9000))
sock.listen()

conn1, addr1 = sock.accept()
conn2, addr2 = sock.accept()

conn1.setblocking(0)
conn2.setblocking(0)

epoll = select.epoll()  # Linux specific
epoll.register(conn1.fileno(), select.EPOLLIN | select.EPOLLOUT)
epoll.register(conn2.fileno(), select.EPOLLIN | select.EPOLLOUT)

conn_map = {
    conn1.fileno(): conn1,
    conn2.fileno(): conn2,
}

with True:
    events = epoll.poll(1)
    for fileno, event in events:
        if event & select.EPOLLIN:
            data = conn_map[fileno].recv(1024)
            print(data.decode("utf8"))
        elif event & select.EPOLLOUT:
            conn_map[fileno].send("ping".encode("utf8"))
