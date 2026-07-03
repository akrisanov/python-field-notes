"""
Since our problem is that an executor creates a future instead of a task, and the shutdown
handling inside asyncio.run() deals with tasks, our next plan is to wrap the future
(produced by the executor) inside a new task object.

Option B: add the executor future to the gathered tasks.
"""
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor


async def make_coro(future):
    """
    The important point here is that we're using create_task(), which means that this task
    will appear in the list of all_tasks() within the shutdown handling of asyncio.run(),
    and will receive a cancellation during the shutdown process.
    """
    try:
        return await future
    except asyncio.CancelledError:
        return await future


async def main():
    loop = asyncio.get_running_loop()

    future = loop.run_in_executor(None, blocking)
    # This code is very clumsy because you have to wrap every executor Future instance
    # inside a make_coro() call.
    asyncio.create_task(make_coro(future))

    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bye!")
