import asyncio
import bisect
from typing import Dict, List, Tuple


class ClientServerProtocol(asyncio.Protocol):
    Metrics = Dict[str, List[Tuple[int, float]]]

    GET_CMD = "get"
    PUT_CMD = "put"
    ALL_KEY = "*"

    OK_RESPONSE = "ok\n\n"
    ERROR_RESPONSE = "error\nwrong command\n\n"

    _metrics = {}

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, command: bytes):
        resp = self._handle_request(command)
        self.transport.write(resp.encode())

    def _handle_request(self, command: bytes) -> str:
        """
        Обрабатывает запрос от клиента.

        :param command: имя команды от клиента
        :return: сериализованный ответ для сервера
        """
        args = command.decode().split()

        if len(args) < 2:
            return self.ERROR_RESPONSE

        if args[0] == self.GET_CMD and len(args) == 2:
            return self._get(metric=args[1])
        elif args[0] == self.PUT_CMD and len(args) == 4:
            return self._put(metric=args[1], value=args[2], timestamp=args[3])

        return self.ERROR_RESPONSE

    def _get(self, metric: str) -> str:
        """
        Получение данных метрик(и).

        :param metric: имя метрики
        :return: сериализованный ответ для сервера
        """
        if metric == self.ALL_KEY:
            return self._serialize(self._metrics)
        elif metric in self._metrics:
            return self._serialize({metric: self._metrics[metric]})

        return self.OK_RESPONSE

    def _serialize(self, data: Metrics) -> str:
        """
        Сериализует данные метрик(и) в строку согласно заданному формату.

        :param data: метрики
        :return: сериализованный ответ для сервера
        """
        if not data:
            return self.OK_RESPONSE

        resp = "ok"

        for metric, values in data.items():
            for timestamp, value in values:
                resp += f"\n{metric} {value} {timestamp}"

        resp += "\n\n"

        return resp

    def _put(self, metric: str, value: str, timestamp: str) -> str:
        """
        Сохраняет метрику.

        :param metric: имя метрики
        :param value: значение
        :param timestamp: временная метка
        :return: сериализованный ответ для сервера
        """
        try:
            value = float(value)
            timestamp = int(timestamp)
        except ValueError:
            return self.ERROR_RESPONSE

        record = (timestamp, value)

        if metric not in self._metrics:
            self._metrics[metric] = [record]
        else:
            # сохраняем последнее значение метрики для временной метки
            for row in self._metrics[metric]:
                if row[0] == timestamp:
                    self._metrics[metric].remove(row)

            bisect.insort(self._metrics[metric], record)

        return self.OK_RESPONSE


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
