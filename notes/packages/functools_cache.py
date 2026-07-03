from functools import cache, lru_cache
import time


# @cache               # Execution time: 0.0009109973907470703 seconds
@lru_cache(maxsize=5)  # Execution time: 0.0012359619140625 seconds
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


def main():
    st = time.time()

    for n in range(400):
        print(n, fib(n))

    et = time.time()
    elapsed_time = et - st
    print("Execution time:", elapsed_time, "seconds")


if __name__ == "__main__":
    main()
