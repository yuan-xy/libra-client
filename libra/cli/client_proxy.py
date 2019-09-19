from libra import Client, WalletLibrary
import pdb

class ClientProxy:
    def __init__(self, client, libra_args):
        self.grpc_client = client
        self.libra_args = libra_args
        self.wallet = WalletLibrary.new()
        self.accounts = self.wallet.accounts

    def print_all_accounts(self):
        if not self.accounts:
            print("No user accounts")
        else:
            for index, account in enumerate(self.accounts):
                print(
                    "User account index: {}, address: {}, sequence number: {}, status:{}".format(
                    index,
                    account.address.hex(),
                    account.sequence_number,
                    account.status
                    )
                )

    def create_next_account(self):
        account = self.wallet.new_account()
        return (self.wallet.child_count-1, account)

    def recover_wallet_accounts(self, filename):
        self.wallet = WalletLibrary.recover(filename)
        self.accounts = self.wallet.accounts
        if self.libra_args.sync:
            for account in self.accounts:
                account.sequence_number = self.grpc_client.get_sequence_number(account.address)
        return self.accounts

    def write_recovery(self, filename):
        self.wallet.write_recovery(filename)

    def mint_coins(self, address_or_refid, libra, is_blocking):
        libra = int(libra)
        address = self.parse_address_or_refid(address_or_refid)
        self.grpc_client.mint_coins_with_faucet_service(address, libra, is_blocking)

    def parse_address_or_refid(self, address_or_refid):
        if len(address_or_refid) == 64:
            return address
        else:
            idx = int(address_or_refid)
            return self.accounts[idx].address.hex()

    def get_balance(self, address_or_refid):
        address = self.parse_address_or_refid(address_or_refid)
        micro_libra = self.grpc_client.get_balance(address)
        return micro_libra / 1_000_000

    def get_sequence_number(self, address_or_refid):
        address = self.parse_address_or_refid(address_or_refid)
        seq = self.grpc_client.get_sequence_number(address)
        return seq




