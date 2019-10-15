from libra.cli.command import *
from libra.json_print import json_print

class AccountCmd(Command):
    def get_aliases(self):
        return ["account", "a"]

    def get_description(self):
        return "Account query by address"

    def execute(self, client, params):
        commands = [
            AccountCmdGetBalance(),
            AccountCmdGetSeqNum(),
            AccountCmdGetLatestAccountState(),
            AccountCmdGetTxnByAccountSeq()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class AccountCmdGetBalance(Command):
    def get_aliases(self):
        return ["balance", "b"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return "Get the current balance of an account by address"

    def execute(self, client, params):
        balance = client.get_balance(params[1])
        json_print({"balance": balance})


class AccountCmdGetSeqNum(Command):
    def get_aliases(self):
        return ["sequence", "s"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return ("Get the current sequence number for an account by address")

    def execute(self, client, params):
        sn = client.get_sequence_number(params[1])
        json_print({"sequence": sn})



class AccountCmdGetLatestAccountState(Command):
    def get_aliases(self):
        return ["state", "as"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return "Get the latest state for an account by address"

    def execute(self, client, params):
        state = client.get_account_state(params[1])
        print(state)



class AccountCmdGetTxnByAccountSeq(Command):
    def get_aliases(self):
        return ["txn_acc_seq", "ts"]

    def get_params_help(self):
        return "<account_address> <sequence_number> <fetch_events=true|false>"

    def get_description(self):
        return ("Get the committed transaction by account and sequence number.  "
         "Optionally also fetch events emitted by this transaction.")

    def execute(self, client, params):
        print("TODO")