import socket
import threading


def handle_request(conn, addr):
    print("Connected client:", addr)
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode("utf8"))


with socket.socket() as sock:
    sock.bind(("127.0.0.1", 9000))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=handle_request, args=(conn, addr))
        t.start()
