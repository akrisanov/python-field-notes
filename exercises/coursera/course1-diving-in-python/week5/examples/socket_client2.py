import socket

with socket.create_connection(("", 9000), timeout=5) as sock:
    sock.settimeout(2)
    try:
        sock.sendall("ping".encode("utf8"))
    except socket.timeout:
        print("Send data timeout")
    except socket.error as e:
        print("Send data error:", e)
