from time import ctime

from twisted.internet import (
    asyncioreactor,
)  # <- the reactor is the Twisted version of the asyncio loop

asyncioreactor.install()  # <- use the asyncio event loop as its main reactor

from twisted.internet import reactor, defer, task


async def main():  # <- use native coroutines directly in Twisted programs
    for i in range(5):
        print(f"{ctime()} Hello {i}")
        await task.deferLater(
            reactor, 1, lambda: None
        )  # <- alternative to asyncio.sleep(1)


defer.ensureDeferred(
    main()
)  # <- analogous to loop.create_task() or asyncio.ensure_future()
reactor.run()
