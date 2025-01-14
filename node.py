import asyncio

from blockchain.blockchain import Blockchain


def main():
    blockchain = Blockchain()
    while True:
        try:
            text = input()
            blockchain.mine(text)
        except EOFError:
            break
    print(*blockchain.get_blockchain_from_server(), sep="\n")


if __name__ == "__main__":
    main()
