from canoser import Uint64
from libra_client.cli.command import Command, parse_bool
from libra_client.error import AccountError


class QueryCommand(Command):
    def get_aliases(self):
        return ["query", "q"]

    def get_description(self):
        return "Query operations"

    def execute(self, client, params, **kwargs):
        commands = [
            QueryCommandGetBalance(),
            QueryCommandGetSeqNum(),
            QueryCommandGetLatestAccountState(),
            QueryCommandGetTxnByAccountSeq(),
            QueryCommandGetTxnByRange(),
            QueryCommandGetEvent()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:], **kwargs)


class QueryCommandGetBalance(Command):
    def get_aliases(self):
        return ["balance", "b"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address>"

    def get_description(self):
        return "Get the current balance of an account"

    def execute(self, client, params, **kwargs):
        try:
            balance = client.get_balance(params[1])
            print(f"Balance is: {balance}")
        except AccountError:
            print(f"Failed to get balance: No account exists at {params[1]}")


class QueryCommandGetSeqNum(Command):
    def get_aliases(self):
        return ["sequence", "s"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> [reset_sequence_number=true|false]"

    def get_description(self):
        return ("Get the current sequence number for an account, "
                "and reset current sequence number in CLI (optional, default is false)")

    def execute(self, client, params, **kwargs):
        print(">> Getting current sequence number")
        try:
            sn = client.get_sequence_number(params[1])
            # TODO: support reset_sequence_number
            print(f"Sequence number is: {sn}")
        except AccountError:
            print(f"Failed to get sequence number: No account exists at {params[1]}")


class QueryCommandGetLatestAccountState(Command):
    def get_aliases(self):
        return ["account_state", "as"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address>"

    def get_description(self):
        return "Get the latest state for an account"

    def execute(self, client, params, **kwargs):
        print(">> Getting latest account state")
        state = client.get_latest_account_state(params[1])
        print(
            f"Latest account state is: \n \
            Account: {params[1]}\n \
            State: {state}\n"
        )


class QueryCommandGetTxnByAccountSeq(Command):
    def get_aliases(self):
        return ["txn_acc_seq", "ts"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> <sequence_number> <include_events=true|false>"

    def get_description(self):
        return ("Get the committed transaction by account and sequence number.  "
                "Optionally also fetch events emitted by this transaction.")

    def execute(self, client, params, **kwargs):
        print(">> Getting committed transaction by account and sequence number")
        include_events = parse_bool(params[3])
        transaction = client.get_committed_txn_by_acc_seq(params[1], params[2], include_events)
        print(f"Committed transaction: {transaction}")  # transaction pretty print
        if transaction is None:
            print("Transaction not available")
        elif len(transaction.events) == 0:
            print("no events emitted")


class QueryCommandGetTxnByRange(Command):
    def get_aliases(self):
        return ["txn_range", "tr"]

    def get_params_help(self):
        return "<start_version> <limit> <include_events=true|false>"

    def get_description(self):
        return ("Get the committed transactions by version range. "
                "Optionally also fetch events emitted by these transactions.")

    def execute(self, client, params, **kwargs):
        print(">> Getting committed transaction by range")
        include_events = parse_bool(params[3])
        transactions = client.get_committed_txn_by_range(params[1], params[2], include_events)
        cur_version = Uint64.int_safe(params[1])
        for index, signed_tx in enumerate(transactions):
            # TODO: events print
            print(f"Transaction at version {cur_version+index}: {signed_tx}")


class QueryCommandGetEvent(Command):
    def get_aliases(self):
        return ["event", "ev"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> <sent|received> <start_sequence_number> <ascending=true|false> <limit>"

    def get_description(self):
        return "Get events by account and event type (sent|received)."

    def execute(self, client, params, **kwargs):
        print(">> Getting events by account and event type.")
        ascending = parse_bool(params[4])
        events = client.get_events_by_account_and_type(
            params[1], params[2], params[3], ascending, params[5])
        if not events:
            print("No events returned")
        else:
            for event in enumerate(events):
                print(event)
        # TODO: print("Last event state: {:#?}", last_event_state)
