from blockchain.blockchain import Blockchain


class TestClass():
    bc = Blockchain()

    def test_one(self):
        text = "test"
        self.bc.mine(text)
        block = self.bc.get_last_block_from_server()
        assert block["value"] == text
