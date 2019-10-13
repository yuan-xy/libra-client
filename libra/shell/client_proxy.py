import libra
from libra import Client, WalletLibrary
from libra.account import AccountStatus
from libra.transaction import Script, Module, TransactionPayload, TransactionArgument
from libra.bytecode import get_code_by_filename
from command import parse_bool
import pdb

CLIENT_WALLET_MNEMONIC_FILE = "client.mnemonic"

class ClientProxy:
    def __init__(self, client, libra_args):
        self.grpc_client = client
        self.libra_args = libra_args
        if libra_args.mnemonic_file:
            self.recover_wallet_accounts(libra_args.mnemonic_file)
        else:
            self.wallet = WalletLibrary.new()
            self.wallet.write_recovery(CLIENT_WALLET_MNEMONIC_FILE)
        self.accounts = self.wallet.accounts
        if libra_args.faucet_account_file:
            if libra_args.host == 'ac.testnet.libra.org':
                print("[ERROR] faucet_account_file can't be used with testnet, need `host` to be set.")
                exit(1)
            with open(libra_args.faucet_account_file, 'rb') as f:
                data = f.read()
                assert len(data) == 80
                assert b' \x00\x00\x00\x00\x00\x00\x00' == data[0:8]
                assert b' \x00\x00\x00\x00\x00\x00\x00' == data[40:48]
                private_key = data[8:40]
                public_key = data[48:]
                self.faucet_account = libra.Account.faucet_account(private_key)
                assert self.faucet_account.public_key == public_key
        else:
            self.faucet_account = None

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
        if self.faucet_account:
            print(
                "Faucet account address: {}, sequence_number: {}, status: {}".format(
                self.faucet_account.address_hex,
                self.faucet_account.sequence_number,
                self.faucet_account.status
                )
            )

    @property
    def verbose(self):
        return self.libra_args.verbose

    def create_next_account(self):
        account = self.wallet.new_account()
        return (self.wallet.child_count-1, account)

    def recover_wallet_accounts(self, filename):
        self.wallet = WalletLibrary.recover(filename)
        self.accounts = self.wallet.accounts
        if self.libra_args.sync:
            for account in self.accounts:
                account.sequence_number = self.grpc_client.get_sequence_number(account.address)
                account.status = AccountStatus.Persisted
        return self.accounts

    def write_recovery(self, filename):
        self.wallet.write_recovery(filename)

    def mint_coins(self, address_or_refid, libra, is_blocking):
        micro_libra = int(libra) * 1_000_000
        address = self.parse_address_or_refid(address_or_refid)
        if self.faucet_account:
            self.grpc_client.mint_coins_with_faucet_account(self.faucet_account, address, micro_libra, is_blocking)
        else:
            self.grpc_client.mint_coins_with_faucet_service(address, micro_libra, is_blocking)

    def parse_address_or_refid(self, address_or_refid):
        if len(address_or_refid) == 64:
            return address_or_refid
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
        if len(blob.__str__()) > 0:
            blob = libra.AccountState.deserialize(blob.blob)
        #TODO: update local account if address in local wallet.
        return (blob, address, version)

    def get_committed_txn_by_acc_seq(self, address_or_refid, seq, fetch_events):
        address = self.parse_address_or_refid(address_or_refid)
        seq = int(seq)
        transaction, _usecs = self.grpc_client.get_account_transaction_proto(address, seq, fetch_events)
        return transaction

    def get_committed_txn_by_range(self, start, limit, fetch_events):
        start = int(start)
        limit = int(limit)
        transactions = self.grpc_client.get_transactions(start, limit)
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

    def address_or_refid_to_account(self, address_or_refid):
        sender_addr = self.parse_address_or_refid(address_or_refid)
        _index, account = self.wallet.find_account_by_address_hex(sender_addr)
        if account is None:
            raise IOError(f"address {sender} not in wallet.")
        return account

    def transfer_coins(self, sender, recevier, coin, max_gas, unit_price, is_blocking):
        account = self.address_or_refid_to_account(sender)
        recevier = self.parse_address_or_refid(recevier)
        micro_libra = int(coin) * 1_000_000
        self.grpc_client.transfer_coin(account, recevier, micro_libra, max_gas, unit_price, is_blocking)
        return account.sequence_number

    def execute_script(self, address_or_refid, code_file, script_args):
        account = self.address_or_refid_to_account(address_or_refid)
        code = get_code_by_filename(code_file)
        arguments = [TransactionArgument.parse_as_transaction_argument(x) for x in script_args]
        payload = TransactionPayload('Script', Script(code, arguments))
        self.grpc_client.submit_payload(account, payload, is_blocking=True)

    def publish_module(self, address_or_refid, module_file):
        account = self.address_or_refid_to_account(address_or_refid)
        code = get_code_by_filename(module_file)
        payload = TransactionPayload('Module', Module(code))
        self.grpc_client.submit_payload(account, payload, is_blocking=True)

