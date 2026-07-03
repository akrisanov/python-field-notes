import bisect
import socket
import time
from typing import Dict, List, Tuple, Union


class ClientError(Exception):
    """Исключение, возникающее в случае неуспешного получения данных от сервера метрик."""


class Client:
    Response = Union[Tuple[str, dict], Tuple[str, str]]
    Metrics = Dict[str, List[Tuple[int, float]]]

    SUCCESS_STATUS = "ok"
    ERROR_STATUS = "error"

    def __init__(self, host: str, port: int, timeout: int = None):
        """
        Создание сокета для соединения с сервером.

        :param host:
        :param port:
        :param timeout: необязательный параметр
        """
        try:
            self.sock = socket.create_connection((host, port), timeout=timeout)
        except socket.error as e:
            raise ClientError("Cannot create a new connection to the server.", e)

    def _send(self, command):
        """
        Отправляет сообщение на сервер.

        :param command: имя команды
        """
        try:
            self.sock.sendall(command)
        except socket.error as e:
            raise ClientError(f"Cannot send the {command} command:", e)

    def _recv(self):
        b = b""

        while not b.endswith(b"\n\n"):
            try:
                b += self.sock.recv(1024)
            except socket.error as e:
                raise ClientError(f"Cannot receive data from the server:", e)

        return b

    def __del__(self):
        self.sock.close()

    @staticmethod
    def check_error(status: str, message: str):
        """
        Выбрасывает исключение в случае статуса ошибки.

        :param message: сообщение ошибки
        :param status: статус ответа
        """
        if status == Client.ERROR_STATUS:
            raise ClientError(message)

    @staticmethod
    def ensure_status(payload: list) -> str:
        """
        Возвращает значение статуса или выбрасывает исключение в случае
        невалидных данных.

        :param payload: ответ сервера
        """
        value = payload[0]

        if value not in [Client.SUCCESS_STATUS, Client.ERROR_STATUS]:
            raise ClientError("wrong status")
        return value

    @staticmethod
    def ensure_metric_data(metric: str) -> List[str]:
        """
        Возвращает список name, value, timestamp метрики.
        Выкидывает исключения в случае ошибок форматов данных метрики.

        :param metric: строка данных метрики
        """
        row = metric.split(" ")

        if not len(row) == 3:
            raise ClientError("wrong data")

        # if not len(row[0].split(".")) == 2:  # check metric name
        #     raise ClientError("wrong command")

        return row

    @staticmethod
    def deserialize(raw_data: bytes) -> Response:
        """
        Десериализует ответы сервера.

        Компоненты ответа:

        - статус: `ok` или `error`
        - данные ответа
        - два символа переноса строки

        :param raw_data: массив байт, полученный от сервера
        :return: статуса ответа сервера и сам ответ
        """
        data = list(filter(bool, raw_data.decode().split("\n")))
        status = Client.ensure_status(data)
        payload = {}

        if status == Client.ERROR_STATUS and len(data) == 2:
            payload = data[1]  # error message
        elif status == Client.SUCCESS_STATUS and len(data) >= 2:
            for metric in data[1:]:
                name, value, timestamp = Client.ensure_metric_data(metric)
                typed_metric = (int(timestamp), float(value))

                if name not in payload:
                    payload[name] = []

                bisect.insort(payload[name], typed_metric)

        return status, payload

    def get(self, metric: str = "*") -> Dict[str, List[Tuple[int, float]]]:
        """
        Получает данные метрик с сервера.

        :param metric: название метрики или символ `*` для всех метрик
        :return: словарь с метриками в случае успешного получения ответа от сервера и выбрасывает
        исключение `ClientError` в случае не успешного.
        """
        command = f"get {metric}\n".encode()
        self._send(command)

        raw_data = self._recv()
        status, payload = self.deserialize(raw_data)
        self.check_error(status, payload)

        return payload

    def put(self, metric: str, value: float, timestamp=None) -> None:
        """
        Отправляет данные метрик на сервер.

        :param metric: название метрики
        :param value: численное значение
        :param timestamp: временная метка
        """
        timestamp = timestamp or int(time.time())
        command = f"put {metric} {value} {timestamp}\n".encode()
        self._send(command)

        raw_resp = self._recv()
        status, payload = self.deserialize(raw_resp)
        self.check_error(status, payload)

    def close(self):
        try:
            self.sock.close()
        except socket.error as e:
            raise ClientError("Cannot close the connection:", e)


if __name__ == "__main__":
    client = Client("127.0.0.1", 8888, timeout=15)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))
