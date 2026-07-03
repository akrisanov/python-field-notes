import asyncio
import time


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


loop = asyncio.get_event_loop()
task = loop.create_task(main())
# blocks the current/main thread
# run_until_complete() will keep the loop running only until the given coro completes
# but all other tasks scheduled on the loop will also run while the loop is running
loop.run_until_complete(task)
# gather the still-pending tasks
pending = asyncio.all_tasks(loop=loop)
for task in pending:
    # cancel them
    task.cancel()
group = asyncio.gather(*pending, return_exceptions=True)
# ..and run again until those tasks are done
loop.run_until_complete(group)
# called on a stopped loop: clear all queues and shut down the executor
# a stopped loop can be restarted, but a closed loop is gone for good
loop.close()
