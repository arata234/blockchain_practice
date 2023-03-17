from ecdsa import NIST256p
from ecdsa import SigningKey

import utils

import hashlib
import base58
import codecs

class Wallet(object):
    
    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()
    
    @property
    def public_key(self):
        return self._public_key.to_string().hex()
    
    @property
    def blockchain_address(self):
        return self._blockchain_address
    
    def generate_blockchain_address(self):
        public_key_bytes = self._public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        ripemd160_bpk = hashlib.new("ripemd160")
        ripemd160_bpk.update(sha256_bpk_digest)
        ripemd160_bpk_digest = ripemd160_bpk.digest()
        ripemd160_bpk_hex = codecs.encode(ripemd160_bpk_digest, "hex")

        network_byte = b"00"
        network_coin_key = network_byte + ripemd160_bpk_hex
        network_coin_key_bytes = codecs.decode(
            network_coin_key, "hex"
        )

        sha256_bpk = hashlib.sha256(network_coin_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_bpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_bpk_digest = sha256_2_bpk.digest()
        sha256_hex = codecs.encode(sha256_2_bpk_digest, "hex")

        checksum = sha256_hex[:8]

        address_hex = (network_coin_key + checksum).decode("utf-8")

        blockchain_address = base58.b58encode(address_hex).decode("utf-8")
        return blockchain_address
    
class Transaction(object):
    
    def __init__(self, sender_private_key, sender_public_key,
                 sender_blockchain_address, recipient_blockchain_address,
                 value):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_blockchain_key = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value
        
    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = utils.sorted_dict_by_key({
            "sender_blockchain_address": self.sender_blockchain_key,
            "recipient_blockchain_address": self.recipient_blockchain_address,
            "value": float(self.value)
        })
        sha256.update(str(transaction).encode("utf-8"))
        print(sha256)
        message = sha256.digest()
        print(message)
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p)
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature
    
        
if __name__ == "__main__":
    wallet_M = Wallet()
    wallet_A = Wallet()
    t = Transaction(
        wallet_M.private_key, wallet_M.public_key, wallet_M.blockchain_address,
        wallet_A.blockchain_address, 1.0)
    
    import blockchain
    block_chain = blockchain.BlockChain(
        blockchain_address=wallet_M.blockchain_address)
    block_chain.mining()
    is_added = block_chain.add_transaction(
        wallet_M.blockchain_address,
        wallet_A.blockchain_address,
        1.0,
        wallet_M.public_key,
        t.generate_signature())
    print("Added?", is_added)
    utils.pprint(block_chain.chain)
    
    print("M", block_chain.calculate_total_amount(wallet_M.blockchain_address))
    print("A", block_chain.calculate_total_amount(wallet_A.blockchain_address))