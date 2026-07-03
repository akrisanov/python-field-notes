"""aiohttp brings all things HTTP to asyncio, including support for HTTP clients and servers,
as well as WebSocket support."""

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
app.router.add_get("/", hello)
web.run_app(app, port=8080)
