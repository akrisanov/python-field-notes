"""The collection layer: this server collects process stats."""

import asyncio
from contextlib import suppress
import zmq
import zmq.asyncio
import aiohttp
from aiohttp import web
from aiohttp_sse import sse_response
from weakref import WeakSet
import json

# zmq.asyncio.install()
ctx = zmq.asyncio.Context()

# Each connected client will have an associated Queue() instance,
# so this connections identifier is really a set of queues.
connections = WeakSet()


async def collector():
    sock = ctx.socket(zmq.SUB)  # This ØMQ socket can only receive
    sock.setsockopt_string(zmq.SUBSCRIBE, "")  # we provide empty topic name
    # each of our application-layer instances will be connecting
    # to the same collection server domain name, it's why we need bind here, not connect
    sock.bind("tcp://*:5555")

    with suppress(asyncio.CancelledError):
        while data := await sock.recv_json():
            # getting deserialized messages (dict) from the socket
            print(data)
            for q in connections:
                # As soon as the data comes in, it will be sent to the connected web client:
                await q.put(data)
    sock.close()


async def feed(request):
    """Create coroutines for each connected web client."""
    # the entry will automatically be removed from connections when the queue goes
    # out of scope — i.e., when a web client disconnects.
    queue = asyncio.Queue()
    connections.add(queue)

    with suppress(asyncio.CancelledError):
        async with sse_response(request) as resp:
            while data := await queue.get():
                print("sending data:", data)
                await resp.send(json.dumps(data))  # push data to the web client
    return resp


async def index(request):
    return aiohttp.web.FileResponse("./charts.html")


async def start_collector(app):
    app["collector"] = app.loop.create_task(collector())


async def stop_collector(app):
    print("Stopping collector...")
    app["collector"].cancel()
    await app["collector"]
    ctx.term()


if __name__ == "__main__":
    app = web.Application()

    app.router.add_route("GET", "/", index)
    app.router.add_route("GET", "/feed", feed)

    app.on_startup.append(start_collector)
    app.on_cleanup.append(stop_collector)

    web.run_app(app, host="127.0.0.1", port=8088)
