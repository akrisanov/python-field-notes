import threading


class Point:
    def __init__(self):
        self._mutex = threading.RLock()  # can acquire a mutex twice in the same thread
        self._x = 0
        self._y = 0

    def get(self):
        # prefer context manager over manual calls of acquire() and release() methods
        with self._mutex:
            return self._x, self._y

    def set(self, x, y):
        with self._mutex:
            self._x = x
            self._y = y
