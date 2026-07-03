# read more https://peps.python.org/pep-0530/
import asyncio


async def f(x):
    await asyncio.sleep(0.1)
    return x + 100


async def factory(n):
    for x in range(n):
        await asyncio.sleep(0.1)
        yield f, x


async def main():
    # it's the `async for` that makes a comprehension an async comprehension,
    # not the presence of `await`:
    results = [await f(x) async for f, x in factory(3)]
    print("result = ", results)


asyncio.run(main())
