import socket

sock = socket.socket()
sock.connect(("127.0.0.1", 9000))
# ^ one-liner: sock = socket.create_connection(("127.0.0.1", 9000))
sock.sendall("ping".encode("utf8"))
sock.close()
