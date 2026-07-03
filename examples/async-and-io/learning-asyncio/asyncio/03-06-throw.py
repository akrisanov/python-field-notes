import asyncio


async def f():
    await asyncio.sleep(1.0)
    return 123


coro = f()
coro.send(None)
# raise an exception inside the coroutine, at the await point
coro.throw(Exception, "cancelled")
