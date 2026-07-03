import socket

sock = socket.socket()
sock.bind(("127.0.0.1", 8888))
sock.listen(1)
conn, addr = sock.accept()

print("Соединение установлено:", addr)

# response = b"ok\npalm.cpu 10.5 1501864247\neardrum.cpu 15.3 1501864259\n\n"
# response = b"error\nwrong command\n\n"
# response = b"ok\nserver_wrong_answer_1 15 1111\n\n"
response = b"ok\nunsorted_data 13.045 1501865247\nunsorted_data 10.5 1501864247\nunsorted_data 11.0 1501864243\nunsorted_data 22.5 1501864248\n\n"

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break

        request = data.decode("utf-8")
        print(f"Получен запрос: {ascii(request)}")

        print(f"Отправлен ответ {ascii(response.decode('utf-8'))}")
        conn.send(response)
except KeyboardInterrupt:
    conn.close()
