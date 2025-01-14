import asyncio

from blockchain.blockchain import Blockchain


def main():
    text = "another text"
    blockchain.mine(text)
    print(*blockchain.get_blockchain_from_server(), sep="\n")


if __name__ == "__main__":
    main()
