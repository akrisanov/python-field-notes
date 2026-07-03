import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        # handle the exception and return normally with StopIteration
        print("The coroutine has been cancelled!")
    else:
        return 111


coro = f()
coro.send(None)
coro.send(None)
coro.throw(asyncio.CancelledError)
