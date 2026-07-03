from concurrent.futures import Future
import threading

future0 = Future()
future1 = Future()


def count(future):
    # doing some useful work
    future.set_result(1)


t0 = threading.Thread(target=count, args=(future0,))
t1 = threading.Thread(target=count, args=(future1,))
t0.start()
t1.start()

# blocks until all threads resolve their futures
counter = future0.result() + future1.result()

print(f"Counter: {counter}")
