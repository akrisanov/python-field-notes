# read more https://docs.python.org/3.7/library/contextlib.html#contextlib.asynccontextmanager
from contextlib import asynccontextmanager


async def download_webpage(url):
    ...


async def update_stats(url):
    ...


def process(data):
    ...


@asynccontextmanager
async def web_page(url):
    """an asynchronous generator function"""
    data = await download_webpage(url)
    yield data  # <- asynchronous generator
    await update_stats(url)


async def main():
    async with web_page("google.com") as data:
        process(data)
