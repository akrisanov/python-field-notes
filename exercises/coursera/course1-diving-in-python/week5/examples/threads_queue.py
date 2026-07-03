from queue import Queue
from threading import Thread


def worker(q, n):
    while True:
        item = q.get()
        if item is None:
            break
        print(f"Processing data '{item}' from the queue #{n}")


q = Queue(5)
t1 = Thread(target=worker, args=(q, 1))
t2 = Thread(target=worker, args=(q, 2))
t1.start()
t2.start()

for i in range(50):
    q.put(i)  # blocks until queue has a space for a new item

q.put(None)
q.put(None)
t1.join()
t2.join()
