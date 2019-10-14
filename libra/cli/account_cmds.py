from libra.cli.command import *

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
        if len(params) != 2:
            print("Invalid number of arguments for balance query")
            return
        try:
            balance = client.get_balance(params[1])
            print(f"Balance is: {balance}")
        except Exception as err:
            report_error("Failed to get balance", err, client.verbose)


class AccountCmdGetSeqNum(Command):
    def get_aliases(self):
        return ["sequence", "s"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return ("Get the current sequence number for an account by address")

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for sequence number query")
            return
        try:
            sn = client.get_sequence_number(params[1])
            print(f"Sequence number is: {sn}")
        except Exception as err:
            report_error("Error getting sequence number", err, client.verbose)



class AccountCmdGetLatestAccountState(Command):
    def get_aliases(self):
        return ["state", "as"]

    def get_params_help(self):
        return "<account_address>"

    def get_description(self):
        return "Get the latest state for an account by address"

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for account_state query")
            return
        try:
            state = client.get_account_state(params[1])
            print(state)
        except Exception as err:
            report_error("Error getting latest account state", err, client.verbose)



class AccountCmdGetTxnByAccountSeq(Command):
    def get_aliases(self):
        return ["txn_acc_seq", "ts"]

    def get_params_help(self):
        return "<account_address> <sequence_number> <fetch_events=true|false>"

    def get_description(self):
        return ("Get the committed transaction by account and sequence number.  "
         "Optionally also fetch events emitted by this transaction.")

    def execute(self, client, params):
        if len(params) != 4:
            print("Invalid number of arguments for txn_acc_seq")
            return
        try:
            fetch_events = parse_bool(params[3])
            transaction = client.get_committed_txn_by_acc_seq(params[1], params[2], fetch_events)
            print(f"Committed transaction: {transaction}") #transaction pretty print
            if transaction.HasField("signed_transaction"):
                print("Events: ")
                for event in transaction.events.events:
                    #TODO: event pretty print
                    print(event)
                if len(transaction.events.events) == 0:
                    print("no events emitted")
            else:
                print("Transaction not available")
        except Exception as err:
            report_error("Error getting committed transaction by account and sequence number", err, client.verbose)
