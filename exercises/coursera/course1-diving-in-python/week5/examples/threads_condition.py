import threading


class Queue:
    def __init__(self, size=5):
        self._size = size
        self._queue = []
        self._mutex = threading.RLock()
        self._empty = threading.Condition(self._mutex)
        self._full = threading.Condition(self._mutex)

    def put(self, value):
        with self._full:
            while len(self._queue) >= self._size:
                self._full.wait()

            self._queue.append(value)
            self._empty.notify()

    def get(self):
        with self._empty:
            while len(self._queue) == 0:
                self._empty.wait()

            value = self._queue.pop(0)
            self._full.notify()
            return value
