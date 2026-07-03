import asyncio


async def hello():
    while True:
        print("Hello, World!")
        await asyncio.sleep(1.0)


loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
