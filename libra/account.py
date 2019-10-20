from nacl.signing import SigningKey
from libra.key_factory import new_sha3_256
from enum import Enum
from libra.account_config import AccountConfig
from libra.account_address import Address
import libra
import os

AccountStatus = Enum('AccountStatus', ('Local','Persisted','Unknown'))

class Account:
    def __init__(self, private_key, address=None, sequence_number=0):
        self._signing_key = SigningKey(private_key)
        self._verify_key = self._signing_key.verify_key
        shazer = new_sha3_256()
        shazer.update(self._verify_key.encode())
        if address is None:
            self.address = shazer.digest()
        else:
            self.address = Address.normalize_to_bytes(address)
        self.sequence_number = sequence_number
        self.status = AccountStatus.Local

    def json_print_fields(self):
        return ["address", "private_key", "public_key"]

    @classmethod
    def faucet_account(cls, private_key):
        return cls(private_key, AccountConfig.association_address())

    @classmethod
    def gen_faucet_account(cls, faucet_account_file):
        if faucet_account_file is None:
            faucet_account_file = cls.faucet_file_path()
        with open(faucet_account_file, 'rb') as f:
            data = f.read()
            assert len(data) == 80
            assert b' \x00\x00\x00\x00\x00\x00\x00' == data[0:8]
            assert b' \x00\x00\x00\x00\x00\x00\x00' == data[40:48]
            private_key = data[8:40]
            public_key = data[48:]
            return cls.faucet_account(private_key)

    @classmethod
    def faucet_file_path(cls):
        curdir = os.path.dirname(libra.__file__)
        return os.path.abspath((os.path.join(curdir, "faucet_key_for_test")))

    def sign(self, message):
        return self._signing_key.sign(message)

    @property
    def address_hex(self):
        return self.address.hex()

    @property
    def public_key(self):
        return self._verify_key.encode()

    @property
    def private_key(self):
        return self._signing_key.encode()

    @property
    def public_key_hex(self):
        return self.public_key.hex()

    @property
    def private_key_hex(self):
        return self.private_key.hex()

