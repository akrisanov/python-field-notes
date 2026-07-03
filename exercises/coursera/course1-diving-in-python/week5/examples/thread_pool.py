from concurrent.futures import ThreadPoolExecutor, as_completed


def sqr(num):
    return num*num


# .shutdown() on exit
with ThreadPoolExecutor(max_workers=3) as pool:
    results = [pool.submit(sqr, i) for i in range(10)]

    for future in as_completed(results):
        print(future.result())
