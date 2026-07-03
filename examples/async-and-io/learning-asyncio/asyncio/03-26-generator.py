import asyncio
from aioredis import create_redis


async def main():
    redis = await create_redis(("localhost", 6379))
    keys = ["Americas", "Africa", "Europe", "Asia"]

    async for value in one_at_a_time(redis, keys):
        print(value)


async def one_at_a_time(redis, keys):
    """asynchronous generator function"""
    for k in keys:
        value = await redis.get(k)
        yield value


asyncio.run(main())
