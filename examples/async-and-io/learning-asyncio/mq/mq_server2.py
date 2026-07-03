"""
Message broker: improved design. Decouple sending and receiving messages;
this will resolve the problem where a slow subscriber would also slow down receiving new messages.
"""

import asyncio
import argparse
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from mq_protocol import read_msg, send_msg

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
# one queue for each sender connection
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHAN_QUEUES: Dict[bytes, Queue] = {}


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info("peername")
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)

    # create a task sending messages for this specific client
    send_task = asyncio.create_task(send_client(writer, SEND_QUEUES[writer]))
    print(f"Remote {peername} subscribed to {subscribe_chan}")

    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            if channel_name not in CHAN_QUEUES:
                # create a new, dedicated Queue for every destination channel
                CHAN_QUEUES[channel_name] = Queue(maxsize=10)
                asyncio.create_task(chan_sender(channel_name))
            # push data to the given channel and go immediately back to listening more data
            # if the queue fills up, we’ll wait here until there is space for the new data (backpressure).
            await CHAN_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f"Remote {peername} connection cancelled.")
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected")
    finally:
        print(f"Remote {peername} closed")

        await SEND_QUEUES[writer].put(None)
        await send_task  # wait for that sender task to finish...

        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscribe_chan].remove(writer)


async def send_client(writer: StreamWriter, queue: Queue):
    while True:
        try:
            data = await queue.get()
        except asyncio.CancelledError:
            continue

        if not data:
            break  # got None, exit from a corotine

        try:
            await send_msg(writer, data)
        except asyncio.CancelledError:
            await send_msg(writer, data)

        writer.close()
        await writer.wait_closed()


async def chan_sender(name: bytes):
    """Responsible for taking data off the channel queue and
    distributing that data to subscribers."""
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[name]
            if not writers:
                await asyncio.sleep(1)
                continue  # wait a bit for subscribers and try again

            if name.startswith(b"/queue"):
                writers.rotate()
                writers = [writers[0]]

            if not (msg := await CHAN_QUEUES[name].get()):
                break  # got None, exit from a corotine

            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f"Sending to {name}: {msg[:19]}...")
                    await SEND_QUEUES[writer].put(msg)  # put data in subscriber queues


async def main(args):
    server = await asyncio.start_server(client, host=args.host, port=args.port)
    print("Started the MQ server...")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    # python mq_server.py
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=25000)

    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        print("Bye!")
