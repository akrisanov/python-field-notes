import argparse
import asyncio
from random import randint, uniform
from datetime import datetime as dt
from datetime import timezone as tz
from contextlib import suppress
import zmq, zmq.asyncio, psutil

ctx = zmq.asyncio.Context()


async def stats_reporter(color: str):
    """
    This coroutine function will run as a long-lived coroutine,
    continually sending out data to the server process.
    """
    p = psutil.Process()

    # The socet automatically handle all reconnection and buffering logic for us.
    sock = ctx.socket(zmq.PUB)  # <- one-way messages to be sent to another ØMQ socket
    sock.setsockopt(zmq.LINGER, 1)
    sock.connect("tcp://localhost:5555")

    with suppress(asyncio.CancelledError):
        while True:
            await sock.send_json(  # a wrapper around the usual sock.send()
                {
                    "color": color,
                    "timestamp": dt.now(tz=tz.utc).isoformat(),  # ISO 8601 format
                    "cpu": p.cpu_percent(),
                    "mem": p.memory_full_info().rss / 1024 / 1024,
                }
            )
            await asyncio.sleep(1)  # send metrics every second
    sock.close()  # close the socket when we receive a shutdown signal


async def main(args):
    """Out microservice appliction."""
    asyncio.create_task(stats_reporter(args.color))

    # doing some fake work
    leak = []
    with suppress(asyncio.CancelledError):
        while True:
            sum(range(randint(1_000, 10_000_000)))
            await asyncio.sleep(uniform(0, 1))
            leak += [0] * args.leak


# $ backend-app.py --color red &
# $ backend-app.py --color blue --leak 10000 &
# $ backend-app.py --color green --leak 100000 &
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--color", type=str)
    parser.add_argument("--leak", type=int, default=0)
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("Leaving...")
        ctx.term()
