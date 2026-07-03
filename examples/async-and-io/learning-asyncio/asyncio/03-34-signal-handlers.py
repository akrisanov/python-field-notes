import asyncio
from signal import SIGINT, SIGTERM


async def main():
    try:
        while True:
            print("<Your app is running>")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # When the cancellation signal is received (initiated by cancelling each of the tasks),
        # there will be a period of 3 seconds where main() will continue running during the
        # run_until_complete() phase of the shutdown process.
        for i in range(3):
            print("<Your app is shutting down...>")
            await asyncio.sleep(1)


def handler(sig):
    """
    This will unblock the loop.run_forever() call and allow pending task collection
    and cancellation, and the run_complete() for shutdown.
    """
    loop.stop()
    print(f"Got signal: {sig!s}, shutting down.")
    # we don’t want another SIGINT or SIGTERM to trigger this handler again
    loop.remove_signal_handler(SIGTERM)
    # a “gotcha”: we can’t simply remove the handler for SIGINT, because if we did that,
    # KeyboardInterrupt would again become the handler for SIGINT
    loop.add_signal_handler(
        SIGINT, lambda: None
    )  # <- makes no effect when we press Ctrl+C more than once


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)  # <- !!!

    loop.create_task(main())
    loop.run_forever()

    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()

    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
