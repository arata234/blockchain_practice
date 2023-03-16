import logging
import sys
import time
import json
import hashlib

import utils

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

class BlockChain(object):
    
    def __init__(self):
        self.transaction_pool = []
        self.chain = []
        self.create_block(0, self.generate_hash([]))
        
    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            "timestamp": time.time(),
            "transaction": self.transaction_pool,
            "nonce": nonce,
            "previous_hash": previous_hash,
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def generate_hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(str(block).encode()).hexdigest()
        

def pprint(chains):
    for i, chain in enumerate(chains):
        print("="*25, "Chain ", i, "="*25)
        for k, v in chain.items():
            print(k, v)
    print("-"*40)
        
if __name__ == "__main__":
    block_chain = BlockChain()
    pprint(block_chain.chain)
    
    
    hash = block_chain.generate_hash(block_chain.chain[-1])
    block_chain.create_block(240, hash)
    pprint(block_chain.chain)
    
    
    hash = block_chain.generate_hash(block_chain.chain[-1])
    block_chain.create_block(100, hash)
    pprint(block_chain.chain)