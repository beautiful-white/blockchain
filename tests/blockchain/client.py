import asyncio


class Client:

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port

    async def connect(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        self.reader = reader
        self.writer = writer

    async def _write(self, message: str | bytes):
        if isinstance(message, str):
            message = message.encode()
        self.writer.write(message)
        await self.writer.drain()

    async def write_and_read(self, msg):
        await self._write(msg)
        data = await self.reader.read(400_000)
        message = data.decode()
        self.writer.close()
        return message

    async def write(self, msg: str = ""):
        await self.connect()
        return await self.write_and_read(msg)


if __name__ == "__main__":
    client = Client('194.247.187.94', 35565)
    run = asyncio.run
    msg = "lst"
    print(run(client.write(msg)))
    msg = "std"
    print(run(client.write(msg)))
    msg = "ehheeh"
    print(run(client.write(msg)))
