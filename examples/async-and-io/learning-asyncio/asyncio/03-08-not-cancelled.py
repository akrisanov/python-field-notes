import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print("Nope!")
        # Don't do this
        while True:
            await asyncio.sleep(0)
    else:
        return 111


coro = f()
coro.send(None)
coro.throw(asyncio.CancelledError)
coro.send(None)
