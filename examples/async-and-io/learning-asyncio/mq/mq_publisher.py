import asyncio
import argparse, uuid
from itertools import count
from mq_protocol import send_msg


async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")

    reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
    print(f'I am {writer.get_extra_info("sockname")}')

    # Since we are a sender, we don’t really care about subscribing to any channels.
    # Nevertheless, the protocol requires it, so just provide a null channel to subscribe
    # to (we won’t actually listen for anything).
    channel = b"/null"
    await send_msg(writer, channel)

    chan = args.channel.encode()  # to which channel send messages
    try:
        for i in count():  # simulating while True loop, but with an iteration variable
            await asyncio.sleep(args.interval)  # interval between messages
            data = b"X" * args.size or f"Msg {i} from {me}".encode()  # message payload
            try:
                await send_msg(writer, chan)  # the destination channel name
                await send_msg(writer, data)  # the payload
            except OSError:
                print("Connection ended.")
                break
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    # python mq_publisher.py --channel /queue/testing
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=25000, type=int)
    parser.add_argument("--channel", default="/topic/foo")
    parser.add_argument("--interval", default=1, type=float)
    # The size parameter controls the size of each message payload.
    parser.add_argument("--size", default=0, type=int)

    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        print("Bye!")
