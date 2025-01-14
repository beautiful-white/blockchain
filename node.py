import asyncio

from blockchain.blockchain import Blockchain


def main():
    poetry = ["Ночь, улица, фонарь, аптека,",
              "Бессмысленный и тусклый свет.",
              "Живи ещё хоть четверть века —",
              "Всё будет так. Исхода нет.",
              "Умрёшь — начнёшь опять сначала",
              "И повторится всё, как встарь:",
              "Ночь, ледяная рябь канала,",
              "Аптека, улица, фонарь."
              ]
    blockchain = Blockchain()
    for text in poetry:
        blockchain.mine(text)
    print(*blockchain.get_blockchain_from_server(), sep="\n")


if __name__ == "__main__":
    main()
