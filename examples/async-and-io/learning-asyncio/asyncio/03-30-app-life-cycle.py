# https://docs.python.org/3/library/asyncio-stream.html#tcp-echo-server-using-streams
import asyncio
from asyncio import StreamReader, StreamWriter


async def echo(reader: StreamReader, writer: StreamWriter):
    print("New connection.")
    try:
        while data := await reader.readline():
            writer.write(data.upper())
            await writer.drain()
        print("Leaving Connection.")
    except asyncio.CancelledError:
        print("Connection dropped!")


async def main(host="127.0.0.1", port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()


try:
    # python 03-30-app-life-cycle.py
    # telnet 127.0.0.1 8888
    asyncio.run(main())
except KeyboardInterrupt:
    print("Bye!")
