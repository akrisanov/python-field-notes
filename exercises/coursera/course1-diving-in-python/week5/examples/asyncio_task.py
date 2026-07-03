import asyncio


async def sleep_task(num):
    for i in range(5):
        print(f"Task {num}, iter {i}")
        await asyncio.sleep(1)
    return num

loop = asyncio.get_event_loop()
# NOTE: Task is a subclass of Future
task_list = [loop.create_task(sleep_task(i)) for i in range(2)]
loop.run_until_complete(asyncio.wait(task_list))
# the previous two lines can be replaced by asyncio.gather()
result = loop.run_until_complete(asyncio.gather(
    sleep_task(10),
    sleep_task(20),
))
print(result)
