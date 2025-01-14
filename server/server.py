import asyncio
import structlog
import json
import random

from datetime import datetime
from hashlib import sha256

logger = structlog.getLogger(__name__)

chain = list()
count = 1
block = {
    'timestamp': datetime.now().isoformat(),
    'value': "Momento mori",
    'previous_hash': sha256("genesis".encode("utf-8")).hexdigest(),
    'nonce': format(random.getrandbits(64), "x"),
}
block_hash = sha256(json.dumps(
    block, sort_keys=True).encode("utf-8")).hexdigest()
block["hash"] = block_hash

chain.append(block)

standart = "fe"


def hash(block: dict) -> str:
    """
    Generate a hash of block
    """
    block_string = json.dumps(block, sort_keys=True).encode()
    return sha256(block_string).hexdigest()


def valid_block(block: dict, standart: str = "fefe"):
    """
    Here we validate the block
    """
    try:
        flag1 = block["hash"].startswith(standart)
        _hash = block.pop("hash", None)
        flag2 = hash(block) == _hash
        flag3 = len(block.keys()) == 4
        flag4 = isinstance(block["value"], str)
        flag5 = chain[-1]["hash"] == block["previous_hash"]
        block["hash"] = _hash
        return all([flag1, flag2, flag3, flag4, flag5])
    except:
        return False


async def check_standart():
    global count, standart
    if count % 100 == 0:
        standart = format(random.getrandbits(4 * ((count//100)+3)), "x")
        logger.warn(f"Changed standart: {standart}")


async def handle_echo(reader, writer):
    global count
    data = await reader.read(400_000)
    ip = writer.get_extra_info('peername')[0]
    message: str = data.decode("utf-8").strip()
    if len(message) > 3 and message[0] != "{" and message[-1] != "}" and not message.isdigit():
        writer.write("ERR".encode("utf-8"))
    elif message == "lst":
        writer.write(json.dumps(chain[-1], sort_keys=True).encode("utf-8"))
    elif message == "std":
        writer.write(standart.encode("utf-8"))
    elif message == "cnt":
        writer.write(str(count).encode("utf-8"))
    elif message.isdigit() and int(message) >= 0 and int(message) < count:
        writer.write(json.dumps(
            chain[int(message)], sort_keys=True).encode("utf-8"))
        logger.info(f"SENT {message} block to {ip}")
    else:
        try:
            block = json.loads(message)
            if valid_block(block, standart):
                await check_standart()
                count += 1
                chain.append(block)
                writer.write("ACCEPTED".encode("utf-8"))
                logger.info(f"ACCEPTED NEW BLOCK: {message}")
            else:
                writer.write("INVALID BLOCK".encode("utf-8"))
        except:
            writer.write("INVALID DATA".encode("utf-8"))


async def run_server(ip: str = "localhost", port: int = 35565):
    server = await asyncio.start_server(handle_echo, ip, port)
    logger.info(f"Server started: {ip}/{port}")
    async with server:
        await server.serve_forever()

asyncio.run(run_server("194.247.187.94"))
