import asyncio
from urllib.request import urlopen


def sync_get_url(url):
    return urlopen(url).read()


async def get_url(url, loop=None):
    future = loop.run_in_executor(None, sync_get_url, url)  # creates a new thread to run the function
    resp = await future
    print(len(resp))


loop = asyncio.get_event_loop()
loop.run_until_complete(get_url("https://google.com", loop=loop))
