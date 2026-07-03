"""
TCP is not a message-based protocol: we just get streams of bytes on the wire.
We need to invent our own protocol.
"""

from asyncio import StreamReader, StreamWriter


async def read_msg(stream: StreamReader) -> bytes:
    # get the first 4 bytes, this is the size prefix
    size_bytes = await stream.readexactly(4)
    # those 4 bytes must be converted into an integer
    size = int.from_bytes(size_bytes, byteorder="big")
    # now we know the payload size, so we read that off the stream
    data = await stream.readexactly(size)
    return data


async def send_msg(stream: StreamWriter, data: bytes):
    size_bytes = len(data).to_bytes(4, byteorder="big")
    stream.writelines([size_bytes, data])
    await stream.drain()
