from mnemonic import Mnemonic

import libra
from libra.key_factory import KeyFactory


class WalletLibrary:

    DELIMITER = ";"

    def __init__(self, mnemonic, seed, key_factory, child_number):
        self.mnemonic = mnemonic
        self.seed = seed
        self.key_factory = key_factory
        self.child_number = child_number
        self._recover_accounts()

    def _recover_accounts(self):
        self.accounts = []
        for idx in range(self.child_number):
            privkey = self.key_factory.private_child(idx)
            account = libra.Account(privkey)
            self.accounts.append(account)

    @classmethod
    def new(cls):
        m = Mnemonic("english")
        mnemonic = m.generate(192)
        return cls.new_from_mnemonic(mnemonic)

    @classmethod
    def new_from_mnemonic(cls, mnemonic, child_number=0):
        seed = KeyFactory.to_seed(mnemonic)
        key_factory = KeyFactory(seed)
        return cls(mnemonic, seed, key_factory, child_number)

    @classmethod
    def recover(cls, filename):
        with open(filename) as f:
            data = f.read()
            arr = data.split(WalletLibrary.DELIMITER)
            return cls.new_from_mnemonic(arr[0], int(arr[1]))

    def write_recovery(self, filename):
        with open(filename, 'wt') as f:
            f.write(self.mnemonic)
            f.write(WalletLibrary.DELIMITER)
            f.write(str(self.child_number))
