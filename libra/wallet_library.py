import libra
from libra.key_factory import KeyFactory


class WalletLibrary:

    DELIMITER = ";"
    # def __init__(self):
    #     self.__class__.new_from_mnemonic(file)


    def _recover_accounts(self):
        self.accounts = []
        for idx in range(self.child_number):
            privkey = self.key_factory.private_child(idx)
            account = libra.Account(privkey)
            self.accounts.append(account)


    @classmethod
    def recover(cls, filename):
        with open(filename) as f:
            data = f.read()
            arr = data.split(WalletLibrary.DELIMITER)
            wallet = cls.__new__(cls)
            wallet.mnemonic = arr[0]
            wallet.child_number = int(arr[1])
            wallet.seed = KeyFactory.to_seed(wallet.mnemonic)
            wallet.key_factory = KeyFactory(wallet.seed)
            wallet._recover_accounts()
            return wallet

    def write_recovery(self, filename):
        with open(filename, 'wt') as f:
            f.write(self.mnemonic)
            f.write(WalletLibrary.DELIMITER)
            f.write(str(self.child_number))



    # @classmethod
    # def new_from_mnemonic(file):
    #     key_fac = libra.KeyFactory.read_wallet_file('test/test.wallet')


    #     let seed = Seed::new(&mnemonic, "LIBRA");
    #     WalletLibrary {
    #         mnemonic,
    #         key_factory: KeyFactory::new(&seed).unwrap(),
    #         addr_map: HashMap::new(),
    #         key_leaf: ChildNumber(0),
    #     }