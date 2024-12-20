import json
import random

from datetime import datetime
from hashlib import sha256


class Blockchain(object):
    """
    Blockchain class
    """

    standart = "fefe"
    index = 0

    def __init__(self):
        """
        Init genesis block
        """
        self.chain = []
        self.pending_transactions = []

        print("Creating genesis block")
        self.chain.append(self.new_block())

    def new_block(self, previous_hash: str = None) -> dict:
        """
        Create a block mazafaka
        """
        block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(),
            'transactions': self.pending_transactions,
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

    def last_block(self):
        """
        Get last block of chain
        """
        return self.chain[-1] if self.chain else None

    def get_standart(self):

        return self.standart

    def proof_of_work(self):
        """
        Mine, mine, mine!!!!
        """
        while True:
            new_block = self.new_block(self.last_block()["hash"])
            if self.valid_block(new_block, self.get_standart()):
                break
        self.pending_transactions = []
        self.chain.append(new_block)
        print("[!] Found a new block: ", new_block)

    @staticmethod
    def valid_block(block: dict, standart: str = "fefe"):
        """
        Here we validate the block
        """
        return block["hash"].startswith(standart)

    def get_pendings(self):
        self.pending_transactions = [f"sent you {random.randint(100,5000)} dollars"
                                     for _ in range(random.randint(1, 10))]

    def lets_mine(self):
        while True:
            self.get_pendings()
            self.proof_of_work()
