import asyncio
import time


async def main():
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


# creates a new event loop every time you call it
# asyncio.run() does all of the cancelling, gathering, and
# waiting for pending tasks to finish up
asyncio.run(main())
