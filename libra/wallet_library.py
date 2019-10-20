from canoser import Uint16
from mnemonic import Mnemonic
import libra
from libra.key_factory import KeyFactory
from libra.account_address import HEX_ADDRESS_LENGTH

MAX_CHILD_COUNT = Uint16.max_value

class WalletLibrary:

    DELIMITER = ";"

    def __init__(self, mnemonic, seed, key_factory, child_count, rotate_keys={}):
        self.mnemonic = mnemonic
        self.seed = seed
        self.key_factory = key_factory
        self.child_count = child_count
        self.rotate_keys = rotate_keys
        self.accounts = []
        if child_count > 0:
            self._recover_accounts()
        for ik, iv in self.rotate_keys.items():
            privkey = self.accounts[iv].private_key
            address = self.accounts[ik].address
            self.accounts[ik] = libra.Account(privkey, address=address)
        #print("rotate_keys:", rotate_keys)

    def json_print_fields(self):
        return ["mnemonic", "seed", "child_count", "accounts.address"]

    def find_account_by_address_hex(self, address):
        for index, account in enumerate(self.accounts):
            if account.address.hex() == address:
                return (index, account)
        return (None, None)

    def find_account_by_publickey_hex(self, pubkey):
        for index, account in enumerate(self.accounts):
            if account.public_key.hex() == pubkey:
                return (index, account)
        return (None, None)

    def rotate_key(self, to_rotate_id, master_id):
        to_rotate_id = Uint16.int_safe(str(to_rotate_id))
        master_id = Uint16.int_safe(str(master_id))
        self.rotate_keys[to_rotate_id] = master_id


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
    def new_from_mnemonic(cls, mnemonic, child_count=0, rotate_keys={}):
        seed = KeyFactory.to_seed(mnemonic)
        key_factory = KeyFactory(seed)
        return cls(mnemonic, seed, key_factory, child_count, rotate_keys)

    @classmethod
    def recover(cls, filename):
        with open(filename) as f:
            data = f.read()
            arr = data.split(WalletLibrary.DELIMITER)
            try:
                rotate_keys = cls.recover_rotate_pairs(filename)
            except FileNotFoundError:
                rotate_keys={}
            return cls.new_from_mnemonic(arr[0], Uint16.int_safe(arr[1]), rotate_keys)

    @classmethod
    def recover_rotate_pairs(cls, filename):
        rotate_keys={}
        with open(filename+".rotate") as f:
            data = f.read()
            arr = data.split(WalletLibrary.DELIMITER)
            if arr[-1] == '':
                arr = arr[0:-1]
            for pair in arr:
                arr2 = pair.split(",")
                if len(arr2) != 2:
                    raise ValueError("rotate file format error.")
                rotate_keys[Uint16.int_safe(arr2[0])] = Uint16.int_safe(arr2[1])
            return rotate_keys

    def write_recovery(self, filename):
        with open(filename, 'wt') as f:
            f.write(self.mnemonic)
            f.write(WalletLibrary.DELIMITER)
            f.write(str(self.child_count))
        self.write_recovery_rotate(filename)

    def write_recovery_rotate(self, filename):
        with open(filename+".rotate", 'wt') as f:
            for k, v in self.rotate_keys.items():
                f.write(str(k))
                f.write(",")
                f.write(str(v))
                f.write(WalletLibrary.DELIMITER)

    def get_account_by_address_or_refid(self, address_or_refid):
        assert 64 == HEX_ADDRESS_LENGTH
        slen = len(address_or_refid)
        if slen > 64 or (slen < 64 and slen > len(str(MAX_CHILD_COUNT))):
            raise ValueError(f"address:{address_or_refid} is not valid.")
        if slen == 64:
            _i, account = self.find_account_by_address_hex(address_or_refid)
            if account is None:
                raise ValueError(f"account:{address_or_refid} not in wallet.")
            return account
        else:
            idx = Uint16.int_safe(address_or_refid)
            if idx >=0 and idx < self.child_count:
                return self.accounts[idx]
            else:
                raise ValueError(f"account index {idx} out of range:{self.child_count}")

