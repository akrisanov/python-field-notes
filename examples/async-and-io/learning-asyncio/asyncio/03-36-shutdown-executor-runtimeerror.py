"""This code examines what happens during shutdown when executor jobs take longer to finish than
all the pending Task instances."""

import time
import asyncio


async def main():
    loop = asyncio.get_running_loop()

    loop.run_in_executor(None, blocking)

    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


def blocking():
    """
    In Python 3.9, the asyncio.run() function has been improved to correctly wait for executor
    shutdown, but at the time of writing, this has not yet been backported to Python 3.8.
    """
    time.sleep(1.5)  # <- will cause a RuntimeError
    print(f"{time.ctime()} Hello from a thread!")


asyncio.run(main())
