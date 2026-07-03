async def get_conn(self, host, port):
    pass


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def main():
    async with Connection("localhost", 9001) as conn:
        # do stuff with conn
        ...
