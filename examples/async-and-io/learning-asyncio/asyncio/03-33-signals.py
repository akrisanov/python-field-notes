import asyncio


async def main():
    while True:
        print("<Your app is running>")
        await asyncio.sleep(1)


# simulating asyncio.run()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    try:
        loop.run_until_complete(task)
    except KeyboardInterrupt:
        print("Got signal: SIGINT, shutting down.")

    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()

    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
