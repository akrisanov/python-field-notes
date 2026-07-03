import socket

# socket can be represented with a domain:port pair

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 5000))
server_socket.listen()

while True:
    print("Waiting for an incoming connection...")
    client_socket, addr = server_socket.accept()  # blocking
    print("Got a connection from", addr)

    while True:
        print("Waiting for a request from the client socket...")
        message_size = 4096  # 4kb
        request = client_socket.recv(message_size)  # blocking!

        if not request:
            break

        sent_message = request.decode().strip()

        response = f'Your message is "{sent_message}"\n'.encode()
        client_socket.send(response)  # send to the buffer, blocks sometimes too

        # To handle a second, third, etc. connection we need to switch the execution to
        # the outer loop again and accept a new client socket. But how?

    print("Closing the client connection...")
    client_socket.close()
