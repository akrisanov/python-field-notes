from ast import arg
import asyncio
import argparse
from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from mq_protocol import read_msg, send_msg

# currently active subscribers
SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info("peername")

    # the first message is a message containing the channel to subscribe to
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    print(f"Remote {peername} subscribed to {subscribe_chan}")

    # An infinite loop, waiting for data from the client (reader)
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            print(f"Sending to {channel_name}: {data[:19]}...")

            # get the deque of subscribers on the target channel
            conns = SUBSCRIBERS[channel_name]

            if conns and channel_name.startswith(b"/queue"):
                # in this case, we send the data to only one of the subscribers, not all of them.
                # This can be used for sharing work between a bunch of workers, rather than
                # the usual pub-sub notification scheme, where all subscribers on a channel
                # get all the messages.
                conns.rotate()  # target only whichever client is first; this changes after every rotation
                conns = [conns[0]]

            # send the message to the subscribers,
            # wait for all of the sending to complete!
            # what happens if we have one very slow client?!
            await gather(*[send_msg(c, data) for c in conns])
            # that slows all message distribution to the speed of the slowest subscriber!
            # solution: decouple receiving messages from distributing them.
    except asyncio.CancelledError:
        print(f"Remote {peername} closing connection.")
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected")
    finally:
        print(f"Remote {peername} closed")
        SUBSCRIBERS[subscribe_chan].remove(writer)  # O(n)


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
