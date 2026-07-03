import socket
import selectors  # platform-agnostic

selector = selectors.DefaultSelector()


def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))  # creates a file in Unix
    server_socket.listen()
    selector.register(server_socket, selectors.EVENT_READ, data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # blocking
    print("Connection from", addr)
    selector.register(client_socket, selectors.EVENT_READ, data=send_message)


def send_message(client_socket):
    message_size = 4096  # 4kb
    request = client_socket.recv(message_size)  # blocking!

    if request:
        sent_message = request.decode().strip()
        response = f'Your message is "{sent_message}"\n'.encode()
        client_socket.send(response)  # send to the buffer, blocks sometimes too
    else:
        selector.unregister(client_socket)
        client_socket.close()


def run_event_loop():
    while True:
        events = selector.select()  # (key, events)

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == "__main__":
    print("The default selector is", type(selector))
    socket_server()
    run_event_loop()
