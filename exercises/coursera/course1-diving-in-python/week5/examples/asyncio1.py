import asyncio


@asyncio.coroutine
def hello():
    while True:
        print("Hello, World!")
        yield from asyncio.sleep(1.0)


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
