from threading import Thread
import time


def count_to_zero(num):
    """
    This example illustrates how bad Python is for such tasks.
    """
    while num > 0:
        num -= 1


# sequential run
ts = time.time()
count_to_zero(100_000_000)
count_to_zero(100_000_000)
print("Sequential run:", time.time() - ts)

# parallel run
ts = time.time()
t1 = Thread(target=count_to_zero, args=(100_000_000,))
t2 = Thread(target=count_to_zero, args=(100_000_000,))
t1.start()
t2.start()
t1.join()
t2.join()
print("Parallel run:", time.time() - ts)
