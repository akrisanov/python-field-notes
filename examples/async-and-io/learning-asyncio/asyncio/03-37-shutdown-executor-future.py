"""Option A: wrap the executor call inside a coroutine."""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor


async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    # The code works, but it places a heavy limitation on lifetime management of the executor
    # function: it implies that you must use a try/finally within every single scope
    # where an executor job is created:
    try:
        print(f"{time.ctime()} Hello!")
        await asyncio.sleep(1.0)
        print(f"{time.ctime()} Goodbye!")
    finally:
        await future  # <- ensure that we wait for the future to be finished before the main() function returns


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bye!")
