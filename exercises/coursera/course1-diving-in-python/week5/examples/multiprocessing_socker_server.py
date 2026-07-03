import multiprocessing
import os
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


def worker(sock):
    while True:
        conn, addr = sock.accept()
        print("Worker pid:", os.getpid())
        t = threading.Thread(target=handle_request, args=(conn, addr,))
        t.start()


with socket.socket() as sock:
    sock.bind(("127.0.0.1", 9000))
    sock.listen()

    worker_count = 3
    worker_list = [multiprocessing.Process(
        target=worker, args=(sock,)) for _ in range(worker_count)]

    for w in worker_list:
        w.start()

    for w in worker_list:
        w.join()
