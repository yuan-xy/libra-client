from command import *

class QueryCommand(Command):
    def get_aliases(self):
        return ["query", "q"]

    def get_description(self):
        return "Query operations"

    def execute(self, client, params):
        commands = [
            QueryCommandGetBalance(),
            QueryCommandGetSeqNum(),
            QueryCommandGetLatestAccountState(),
            QueryCommandGetTxnByAccountSeq(),
            QueryCommandGetTxnByRange(),
            QueryCommandGetEvent()
        ]
        subcommand_execute(params[0], commands, client, params[1:])


class QueryCommandGetBalance(Command):
    def get_aliases(self):
        return ["balance", "b"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address>"

    def get_description(self):
        return "Get the current balance of an account"

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for balance query")
            return
        try:
            balance = client.get_balance(params[1])
            print(f"Balance is: {balance}")
        except Exception as err:
            report_error("Failed to get balance", err)


class QueryCommandGetSeqNum(Command):
    def get_aliases(self):
        return ["sequence", "s"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> [reset_sequence_number=true|false]"

    def get_description(self):
        return ("Get the current sequence number for an account, "
         "and reset current sequence number in CLI (optional, default is false)")

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for sequence number query")
            return
        print(">> Getting current sequence number")
        try:
            sn = client.get_sequence_number(params[1])
            print(f"Sequence number is: {sn}")
        except Exception as err:
            report_error("Error getting sequence number", err)



class QueryCommandGetLatestAccountState(Command):
    def get_aliases(self):
        return ["account_state", "as"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address>"

    def get_description(self):
        return "Get the latest state for an account"

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for account_state query")
            return
        print(">> Getting latest account state")
        try:
            (acc, addr, version) = client.get_latest_account_state(params[1])
            print(
                f"Latest account state is: \n \
                Account: {addr}\n \
                State: {acc}\n \
                Blockchain Version: {version}\n"
            )
        except Exception as err:
            report_error("Error getting latest account state", err)



class QueryCommandGetTxnByAccountSeq(Command):
    def get_aliases(self):
        return ["txn_acc_seq", "ts"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> <sequence_number> <fetch_events=true|false>"

    def get_description(self):
        return ("Get the committed transaction by account and sequence number.  "
         "Optionally also fetch events emitted by this transaction.")

    def execute(self, client, params):
        if len(params) != 4:
            print("Invalid number of arguments for txn_acc_seq")
            return
        print(">> Getting committed transaction by account and sequence number")
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
            report_error("Error getting committed transaction by account and sequence number", err)



class QueryCommandGetTxnByRange(Command):
    def get_aliases(self):
        return ["txn_range", "tr"]

    def get_params_help(self):
        return "<start_version> <limit> <fetch_events=true|false>"

    def get_description(self):
        return ("Get the committed transactions by version range. "
         "Optionally also fetch events emitted by these transactions.")

    def execute(self, client, params):
        if len(params) != 4:
            print("Invalid number of arguments for txn_range")
            return
        try:
            print(">> Getting committed transaction by range")
            fetch_events = parse_bool(params[3])
            transactions = client.get_committed_txn_by_range(params[1], params[2], fetch_events)
            cur_version = int(params[1])
            for index, signed_tx in enumerate(transactions):
                #TODO: events print
                print(f"Transaction at version {cur_version+index}: {signed_tx}")
        except Exception as err:
            report_error("Error getting committed transactions by range", err)




class QueryCommandGetEvent(Command):
    def get_aliases(self):
        return ["event", "ev"]

    def get_params_help(self):
        return "<account_ref_id>|<account_address> <sent|received> <start_sequence_number> <ascending=true|false> <limit>"

    def get_description(self):
        return "Get events by account and event type (sent|received)."

    def execute(self, client, params):
        if len(params) != 6:
            print("Invalid number of arguments for events query")
            return
        try:
            print(">> Getting events by account and event type.")
            events = client.get_events_by_account_and_type(
                params[1], params[2], params[3], params[4], params[5])
            if not events:
                print("No events returned")
            else:
                for event in enumerate(events):
                    print(event)
            #TODO: print("Last event state: {:#?}", last_event_state)
        except Exception as err:
            report_error("Error getting events by access path", err)
