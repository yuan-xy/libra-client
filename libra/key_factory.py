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


