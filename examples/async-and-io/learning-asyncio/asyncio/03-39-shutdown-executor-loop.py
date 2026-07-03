"""Option C: just like camping, bring your own loop and your own executor."""

import time
import asyncio
from concurrent.futures import ThreadPoolExecutor as Executor


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")
    loop.stop()


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


loop = asyncio.get_event_loop()
executor = Executor()  # <- we create our own executor instance
loop.set_default_executor(executor)

loop.create_task(main())
future = loop.run_in_executor(None, blocking)  # <- using our custom instance

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Cancelled")

tasks = asyncio.all_tasks(loop=loop)
for t in tasks:
    t.cancel()

group = asyncio.gather(*tasks, return_exceptions=True)
loop.run_until_complete(group)
executor.shutdown(wait=True)  # <- explicitly wait for all the executor jobs to finish
loop.close()
