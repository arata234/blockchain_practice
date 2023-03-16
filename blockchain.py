import logging
import sys
import time


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):
    
    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, "init")
        
    def create_block(self, nonce, previous_hash):
        block = {
            "timestamp": time.time(),
            "transaction": self.transaction_pool,
            "nonce": nonce,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        self.transaction_pool = []
        return block


def pprint(chains):
    for i, chain in enumerate(chains):
        print("="*25, "Chain ", i, "="*25)
        for k, v in chain.items():
            print(k, v)
    print("-"*40)
        
if __name__ == "__main__":
    block_chain = BlockChain()
    pprint(block_chain.chain)
    block_chain.create_block(240, "hash 1")
    pprint(block_chain.chain)
    block_chain.create_block(100, "hash 2")
    pprint(block_chain.chain)