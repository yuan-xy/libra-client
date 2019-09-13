import hashlib
import hmac
import pdb

class KeyFactory:

    @classmethod
    def to_seed(cls, mnemonic, passphrase="LIBRA"):
        mnemonic = mnemonic.encode("utf-8")
        passphrase = b"LIBRA WALLET: mnemonic salt prefix$" + passphrase.encode("utf-8")
        stretched = hashlib.pbkdf2_hmac("sha3-256", mnemonic, passphrase, 2048)
        return stretched[:64]

    def __init__(self, seed):
        MASTER_KEY_SALT = b"LIBRA WALLET: master key salt$"
        self.master = hmac.new(MASTER_KEY_SALT, seed, digestmod=hashlib.sha3_256).digest()


    #See https://github.com/casebeer/python-hkdf/blob/master/hkdf.py
    def hkdf_expand(self, pseudo_random_key, info=b"", length=32):
        hash=hashlib.sha3_256
        hash_len = hash().digest_size
        length = int(length)
        if length > 255 * hash_len:
            raise Exception("Cannot expand to more than 255 * %d = %d bytes using the specified hash function" %\
                (hash_len, 255 * hash_len))
        blocks_needed = length // hash_len + (0 if length % hash_len == 0 else 1) # ceil
        okm = b""
        output_block = b""
        for counter in range(blocks_needed):
            output_block = hmac.new(pseudo_random_key, output_block + info + bytearray((counter + 1,)),\
                hash).digest()
            okm += output_block
        return okm[:length]

    def private_child(self, child_number):
        INFO_PREFIX = b"LIBRA WALLET: derived key$"
        info = INFO_PREFIX + child_number.to_bytes(8, "little")
        hkdf_expand = self.hkdf_expand(self.master, info, 32)
        return hkdf_expand

    @classmethod
    def read_wallet_file(cls, filename):
        with open(filename) as f:
            data = f.read()
            arr = data.split(";")
            child_number = int(arr[1])
            seed = cls.to_seed(arr[0])
            kfac = cls(seed)
            kfac.child_number = child_number
            return kfac


