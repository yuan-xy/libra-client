from canoser import Uint64
from libra.cli.command import *
from libra.transaction import SignedTransaction
from libra.account_config import AccountConfig
from libra.wallet_library import WalletLibrary

class AccountCmd(Command):
    def get_aliases(self):
        return ["account", "a"]

    def get_description(self):
        return "Account query by address"

    def execute(self, client, params):
        commands = [
            AccountCmdConfig(),
            AccountCmdGetBalance(),
            AccountCmdGetSeqNum(),
            AccountCmdGetLatestAccountState(),
            AccountCmdGetTxnByAccountSeq(),
            AccountCmdMint(),
            AccountCmdRotateAuthenticationKey()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class AccountCmdConfig(Command):
    def get_aliases(self):
        return ["config", "c"]

    def get_description(self):
        return "Show the config of Libra"

    def execute(self, client, params):
        json_print_in_cmd(AccountConfig.all_config(), sort_keys=False)


class AccountCmdGetBalance(Command):
    def get_aliases(self):
        return ["balance", "b"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return "Get the current balance of an account by address"

    def execute(self, client, params):
        balance = client.get_balance(params[1])
        json_print_in_cmd({"balance": balance})


class AccountCmdGetSeqNum(Command):
    def get_aliases(self):
        return ["sequence", "s"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return ("Get the current sequence number for an account by address")

    def execute(self, client, params):
        sn = client.get_sequence_number(params[1])
        json_print_in_cmd({"sequence": sn})



class AccountCmdGetLatestAccountState(Command):
    def get_aliases(self):
        return ["state", "as"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return "Get the latest state for an account by address"

    def execute(self, client, params):
        state = client.get_account_state(params[1])
        json_print_in_cmd(state)


class AccountCmdGetTxnByAccountSeq(Command):
    def get_aliases(self):
        return ["txn_acc_seq", "ts"]

    def get_params_help(self):
        return "<account_address> <sequence_number> <fetch_events=true|false>"

    def get_description(self):
        return ("Get the committed transaction by account and sequence number.  "
         "Optionally also fetch events emitted by this transaction.")

    def execute(self, client, params):
        fetch_events = parse_bool(params[3])
        seq = Uint64.int_safe(params[2])
        transaction, _usecs = client.get_account_transaction_proto(params[1], seq, fetch_events)
        json_print_in_cmd(transaction)



class AccountCmdMint(Command):
    def get_aliases(self):
        return ["mint", "mintb", "m", "mb"]

    def get_params_help(self):
        return "<receiver_account_address> <number_of_micro_libra>"

    def get_description(self):
        return "Mint micro_libra to the address. Suffix 'b' is for blocking"

    def execute(self, client, params):
        is_blocking = blocking_cmd(params[0])
        resp = client.mint_coins(params[1],Uint64.int_safe(params[2]), is_blocking)
        json_print_in_cmd({"sequence_number": resp})



class AccountCmdRotateAuthenticationKey(Command):
    def get_aliases(self):
        return ["rotate_auth_key", "rak"]

    def get_params_help(self):
        return "<sender_account_id_in_wallet>|<address> <public_key> <mnemonic_file_path>"

    def get_description(self):
        return "Rotate the authentication key of account in wallet."

    def execute(self, client, params):
        wallet = WalletLibrary.recover(params[3])
        account = wallet.get_account_by_address_or_refid(params[1])
        client.rotate_authentication_key(account, params[2])
        index, _account = wallet.find_account_by_publickey_hex(params[2])
        wallet.rotate_key(params[1], index)
        wallet.write_recovery(params[3])
        #TODO: Exec Transaction throw major_status: 2, after rotate key.
        # account_resource = client.get_account_resource(account.address)
        # key = account_resource.to_json_serializable()["authentication_key"]
        json_print_in_cmd({
            "address": account.address_hex,
            "authentication_key": params[2]})

