import asyncio
import argparse, uuid
from mq_protocol import read_msg, send_msg


async def main(args):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")

    reader, writer = await asyncio.open_connection(args.host, args.port)

    print(f'I am {writer.get_extra_info("sockname")}')
    channel = args.listen.encode()

    await send_msg(writer, channel)  # subscribe to a channel

    try:
        while data := await read_msg(reader):
            print(f"Received by {me}: {data[:20]}")  # reading messages from the channel
        print("Connection ended.")
    except asyncio.IncompleteReadError:
        print("Server closed.")
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    # python mq_subscriber.py --listen /queue/testing
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=25000)
    parser.add_argument("--listen", default="/topic/foo")

    try:
        asyncio.run(main(parser.parse_args()))
    except KeyboardInterrupt:
        print("Bye!")
