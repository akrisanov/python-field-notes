import socket
from select import select

to_watch = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))  # creates a file in Unix
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # blocking
    print("Connection from", addr)
    to_watch.append(client_socket)


def send_message(client_socket):
    message_size = 4096  # 4kb
    request = client_socket.recv(message_size)  # blocking!

    if request:
        sent_message = request.decode().strip()
        response = f'Your message is "{sent_message}"\n'.encode()
        client_socket.send(response)  # send to the buffer, blocks sometimes too
    else:
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_watch, [], [])  # read, write, errors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == "__main__":
    to_watch.append(server_socket)
    event_loop()
