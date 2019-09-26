from libra import Client, WalletLibrary
from command import parse_bool
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
        micro_libra = int(libra) * 1_000_000
        address = self.parse_address_or_refid(address_or_refid)
        self.grpc_client.mint_coins_with_faucet_service(address, micro_libra, is_blocking)

    def parse_address_or_refid(self, address_or_refid):
        if len(address_or_refid) == 64:
            return address
        else:
            idx = int(address_or_refid)
            if idx >=0 and idx < self.wallet.child_count:
                return self.accounts[idx].address.hex()
            else:
                raise IOError(f"account index {idx} out of range:{self.wallet.child_count}")

    def get_balance(self, address_or_refid):
        address = self.parse_address_or_refid(address_or_refid)
        micro_libra = self.grpc_client.get_balance(address)
        return micro_libra / 1_000_000

    def get_sequence_number(self, address_or_refid):
        address = self.parse_address_or_refid(address_or_refid)
        seq = self.grpc_client.get_sequence_number(address)
        #TODO sync seq
        return seq

    def get_latest_account_state(self, address_or_refid):
        address = self.parse_address_or_refid(address_or_refid)
        blob, version = self.grpc_client.get_account_blob(address)
        #update local account if address in local wallet.
        return (blob, address, version)

    def get_committed_txn_by_acc_seq(self, address_or_refid, seq, fetch_events):
        address = self.parse_address_or_refid(address_or_refid)
        seq = int(seq)
        transaction = self.grpc_client.get_account_transaction(address, seq, fetch_events)
        return transaction

    def get_committed_txn_by_range(self, start, limit, fetch_events):
        start = int(start)
        limit = int(limit)
        transactions = self.grpc_client.get_transactions(start, limit, fetch_events)
        return transactions

    def get_events_by_account_and_type(self, address_or_refid, sent_received, start_seq, ascending, limit):
        address = self.parse_address_or_refid(address_or_refid)
        start_seq = int(start_seq)
        limit = int(limit)
        ascending = parse_bool(ascending)
        if sent_received == "sent":
            return self.grpc_client.get_events_sent(address, start_seq, ascending, limit)
        elif sent_received == "received":
            return self.grpc_client.get_events_received(address, start_seq, ascending, limit)
        else:
            raise IOError(f"Unknown event type: {sent_received}, only sent and received are supported")

    def transfer_coins(self, sender, recevier, coin, max_gas, unit_price, is_blocking):
        sender_addr = self.parse_address_or_refid(sender)
        index, account = self.wallet.find_account_by_address_hex(sender_addr)
        if account is None:
            raise IOError(f"address {sender} not in wallet.")
        recevier = self.parse_address_or_refid(recevier)
        micro_libra = int(coin) * 1_000_000
        self.grpc_client.transfer_coin(account, recevier, micro_libra, max_gas, unit_price, is_blocking)
        return (index, account.sequence_number)