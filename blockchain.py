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
        self.create_block(0, self.generate_hash({}))
        
    def create_block(self, nonce, previous_hash):
        block = utils.sorted_dict_by_key({
            "timestamp": time.time(),
            "transactions": self.transaction_pool,
            "nonce": nonce,
            "previous_hash": previous_hash,
        })
        self.chain.append(block)
        self.transaction_pool = []
        return block

    def generate_hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(str(block).encode()).hexdigest()
        
    def add_transaction(self, sender_blockchain_address, 
                        recipient_blockchain_address, value):
        transaction = utils.sorted_dict_by_key({
            "sender_blockchain_address": sender_blockchain_address,
            "recipient_blockchain_address": recipient_blockchain_address,
            "value": float(value),
        })
        self.transaction_pool.append(transaction)
        return True

def pprint(chains):
    for i, chain in enumerate(chains):
        print("="*25, "Chain ", i, "="*25)
        for k, v in chain.items():
            if k == 'transactions':
                print(k)
                for d in v:
                    print("-"*40)
                    for kk, vv in d.items():
                        print(kk, vv)
            else:
                print(k, v)     
    print("*"*40)
        
if __name__ == "__main__":
    block_chain = BlockChain()
    pprint(block_chain.chain)
    
    block_chain.add_transaction("A", "B", 1.0)
    hash = block_chain.generate_hash(block_chain.chain[-1])
    block_chain.create_block(240, hash)
    pprint(block_chain.chain)
    
    block_chain.add_transaction("C", "D", 2.0)
    block_chain.add_transaction("X", "Y", 1.0)
    hash = block_chain.generate_hash(block_chain.chain[-1])
    block_chain.create_block(100, hash)
    pprint(block_chain.chain)