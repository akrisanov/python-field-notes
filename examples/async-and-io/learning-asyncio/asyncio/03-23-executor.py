import asyncio
from contextlib import asynccontextmanager


def download_webpage(url):
    ...


def update_stats(url):
    ...


def process(data):
    ...


@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_event_loop()
    # use the default executor which is a ThreadPoolExecutor
    data = await loop.run_in_executor(None, download_webpage, url)
    yield data  # <- asynchronous generator
    await loop.run_in_executor(None, update_stats, url)


async def main():
    async with web_page("google.com") as data:
        process(data)
