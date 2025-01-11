import json
import random
import asyncio

from datetime import datetime
from hashlib import sha256

from blockchain.client import Client


class Blockchain(object):
    """
    Blockchain class
    """
    standart = ""
    last = dict()
    client = Client('194.247.187.94', 35565)

    def get_standart_from_server(self):
        return asyncio.run(self.client.write("std"))

    def get_last_block_from_server(self):
        """
        Get last block of chain
        """
        return json.loads(asyncio.run(self.client.write("lst")))

    def update(self):
        self.last = self.get_last_block_from_server()
        self.standart = self.get_standart_from_server()

    def send_block_to_server(self, block: dict):
        return asyncio.run(self.client.write(json.dumps(
            block, sort_keys=True).encode("utf-8")))

    def __init__(self, value: str = "No Value"):
        """
        Init genesis block
        """
        self.value = value
        self.standart = self.get_standart_from_server()
        self.last = self.get_last_block_from_server()
        print(self.last)

    def new_block(self, previous_hash: str = None) -> dict:
        """
        Create a block mazafaka
        """
        block = {
            'timestamp': datetime.now().isoformat(),
            'value': self.value,
            'previous_hash': previous_hash,
            'nonce': format(random.getrandbits(64), "x"),
        }
        block_hash = self.hash(block)
        block["hash"] = block_hash

        return block

    @staticmethod
    def hash(block: dict) -> str:
        """
        Generate a hash of block
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    def get_standart(self):
        return self.standart

    def last_block(self):
        return self.last

    def proof_of_work(self, value):
        """
        Mine, mine, mine!!!!
        """

        self.value = value
        while True:
            new_block = self.new_block(self.last_block()["hash"])
            if self.valid_block(new_block, self.get_standart()):
                break
        self.pending_transactions = []
        self.block = new_block
        print("[!] Found a new block: ", new_block)
        server_answer = self.send_block_to_server(new_block)
        print(server_answer)
        self.last = new_block
        if server_answer == "INVALID BLOCK":
            self.update()
            print("Updating standart and last block, repeating...")
            self.proof_of_work(value=value)

    @staticmethod
    def valid_block(block: dict, standart: str = "fefe"):
        """
        Here we validate the block
        """
        return block["hash"].startswith(standart)
