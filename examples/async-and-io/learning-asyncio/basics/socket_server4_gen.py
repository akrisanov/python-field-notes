"""Using generators for async code.

David Beazley
2015 PyCon
Concurrency from the Ground up Live
"""

from select import select
import socket

tasks = []  # can be replaced with a (de)queue
to_read = {}
to_write = {}


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    while True:
        yield ("read", server_socket)

        client_socket, addr = server_socket.accept()  # blocking
        print("Got a connection from", addr)

        tasks.append(handle_connection(client_socket))


def handle_connection(client_socket):
    while True:
        yield ("read", client_socket)

        print("Waiting for a request from the client socket...")
        message_size = 4096  # 4kb
        request = client_socket.recv(message_size)  # blocking

        if not request:
            break

        sent_message = request.decode().strip()
        response = f'Your message is "{sent_message}"\n'.encode()

        yield ("write", client_socket)
        client_socket.send(response)  # send to the buffer, blocks sometimes too

    client_socket.close()


def run_event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == "read":
                to_read[sock] = task

            if reason == "write":
                to_write[sock] = task
        except StopIteration:
            print("All tasks have finished.")


tasks.append(start_server())
run_event_loop()
