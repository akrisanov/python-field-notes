import asyncio
from contextlib import suppress


async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    try:
        # It was possible to do this before Python 3.8, but it is no longer allowed
        f.set_result("I have finished.")
    except RuntimeError as e:
        print(f"No longer allowed: {e}")
        f.cancel()


loop = asyncio.get_event_loop()

fut = asyncio.Task(asyncio.sleep(1_000_000))
print(fut.done())

# It satisfies the type signature of the function because Task is a subclass of Future
loop.create_task(main(fut))

with suppress(asyncio.CancelledError):
    loop.run_until_complete(fut)

print(fut.done())
print(fut.cancelled())
