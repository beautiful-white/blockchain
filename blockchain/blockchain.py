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
    standart: str = ""
    last: dict = dict()
    client: Client = Client('194.247.187.94', 35565)

    def get_standart_from_server(self):
        """
        Get new standart from server
        """
        return asyncio.run(self.client.write("std"))

    def get_last_block_from_server(self):
        """
        Get last block of chain
        """
        return json.loads(asyncio.run(self.client.write("lst")))

    def update(self):
        """
        Get new standart and last mined block
        """
        self.last = self.get_last_block_from_server()
        self.standart = self.get_standart_from_server()

    def send_block_to_server(self, block: dict):
        """
        Send block to server for varification
        """
        return asyncio.run(self.client.write(json.dumps(
            block, sort_keys=True)))  # there was the encode function

    def get_blockchain_from_server(self):
        """
        Get a whole blockchain
        """
        chain: list = list()
        count: int = int(asyncio.run(self.client.write("cnt")))
        for i in range(count):
            block = json.loads(asyncio.run(self.client.write(str(i))))
            chain.append(block)
            print(f"GOT {i} of {count}", end='\r')
        return chain

    def __init__(self):
        """
        Init genesis block
        """
        self.update()

    def new_block(self, previous_hash: str = None) -> dict:
        """
        Create a block 
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
        """
        Get standart
        """
        return self.standart

    def last_block(self):
        """
        Get last block
        """
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

    def mine(self, value: str):
        self.proof_of_work(value=value)

    @staticmethod
    def valid_block(block: dict, standart: str = "fefe"):
        """
        Here we validate the block
        """
        return block["hash"].startswith(standart)
