from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()


def count(_):
    return 1


# like built-in map, but concurrent
counter = sum(executor.map(do_something, range(2)))

print(f"Counter: {counter}")
