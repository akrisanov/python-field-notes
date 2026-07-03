import asyncio
import random
import time

import janus


async def main():
    loop = asyncio.get_running_loop()

    queue = janus.Queue(loop=loop)
    future = loop.run_in_executor(None, data_source, queue)

    while (data := await queue.async_q.get()) is not None:
        print(f"Got {data} off queue")

    print("Done.")


def data_source(queue):
    """The blocking code running in a thread.

    If you can, it's better to aim for having short executor jobs, and in these cases,
    a queue (for communication) won't be necessary. This isn't always possible, though, and
    in such situations, the Janus queue can be the most convenient solution to buffer and
    distribute data between threads and coroutines.
    """
    for i in range(10):
        r = random.randint(0, 4)
        time.sleep(r)
        queue.sync_q.put(r)  # place data into the Janus queue
    queue.sync_q.put(None)  # tell the main cotoutine exit the print loop


asyncio.run(main())
