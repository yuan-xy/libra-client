from mnemonic import Mnemonic

import libra
from libra.key_factory import KeyFactory


class WalletLibrary:

    DELIMITER = ";"

    def __init__(self, mnemonic, seed, key_factory, child_count):
        self.mnemonic = mnemonic
        self.seed = seed
        self.key_factory = key_factory
        self.child_count = child_count
        self.accounts = []
        if child_count > 0:
            self._recover_accounts()

    def find_account_by_address_hex(self, address):
        for index, account in enumerate(self.accounts):
            if account.address.hex() == address:
                return (index, account)
        return (None, None)

    def _recover_accounts(self):
        for idx in range(self.child_count):
            self._add_account(idx)

    def _add_account(self, account_idx):
            privkey = self.key_factory.private_child(account_idx)
            account = libra.Account(privkey)
            self.accounts.append(account)
            return account

    def new_account(self):
        child_index = self.child_count
        self.child_count += 1
        return self._add_account(child_index)


    @classmethod
    def new(cls):
        m = Mnemonic("english")
        mnemonic = m.generate(192)
        return cls.new_from_mnemonic(mnemonic)

    @classmethod
    def new_from_mnemonic(cls, mnemonic, child_count=0):
        seed = KeyFactory.to_seed(mnemonic)
        key_factory = KeyFactory(seed)
        return cls(mnemonic, seed, key_factory, child_count)

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
            f.write(str(self.child_count))
