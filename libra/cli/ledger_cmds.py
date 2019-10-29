from libra.cli.command import *
from libra.wallet_library import WalletLibrary
from libra.transaction import SignedTransaction, Transaction
from datetime import datetime


class LedgerCmd(Command):
    def get_aliases(self):
        return ["ledger", "lg"]

    def get_description(self):
        return "show ledger info of Libra blockchain"

    def execute(self, client, params):
        commands = [
            LedgerCmdInfo(),
            LedgerCmdTime()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class LedgerCmdInfo(Command):
    def get_aliases(self):
        return ["info", "i"]

    def get_description(self):
        return "Get the latest ledger info of Libra blockchain"

    def execute(self, client, params):
        info = client.get_latest_ledger_info()
        json_print_in_cmd(info)


class LedgerCmdTime(Command):
    def get_aliases(self):
        return ["time", "t"]

    def get_description(self):
        return "Get the start and latest ledger time of Libra blockchain"

    def execute(self, client, params):
        request, resp = client._get_txs(1)
        info = resp.ledger_info_with_sigs.ledger_info
        txnp = resp.response_items[0].get_transactions_response.txn_list_with_proof
        tx = Transaction.deserialize(txnp.transactions[0].transaction)
        stx = tx.value
        start_time = datetime.fromtimestamp(stx.raw_txn.expiration_time)
        latest_time = datetime.fromtimestamp(info.timestamp_usecs / 1000_000)
        json_print_in_cmd({
            "start_time": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "latest_time": latest_time.strftime("%Y-%m-%dT%H:%M:%S")
            }, sort_keys=False)