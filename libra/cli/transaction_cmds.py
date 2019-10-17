from libra.cli.command import *

class TransactionCmd(Command):
    def get_aliases(self):
        return ["transaction", "t"]

    def get_description(self):
        return "Transaction query"

    def execute(self, client, params):
        commands = [
            TransactionCmdGetByVer(),
            TransactionCmdByRange(),
            TransactionCmdGetLatestVer(),
            TransactionCmdGetLatest()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class TransactionCmdGetByVer(Command):
    def get_aliases(self):
        return ["show", "s"]

    def get_params_help(self):
        return "<version number>"

    def get_description(self):
        return "Get the transaction by version"

    def execute(self, client, params):
        tx = client.get_transaction(int(params[1]))
        json_print_in_cmd(tx)


class TransactionCmdByRange(Command):
    def get_aliases(self):
        return ["range", "r"]

    def get_params_help(self):
        return "<start_version> <limit> [fetch_events=true|false]"

    def get_description(self):
        return ("Get up to <limit> number transactions from <start_version>")

    def execute(self, client, params):
        sn = client.get_transactions(int(params[1]), int(params[2]))
        json_print_in_cmd([x.to_json_serializable() for x in sn])


class TransactionCmdGetLatestVer(Command):
    def get_aliases(self):
        return ["latest_version", "lv"]

    def get_description(self):
        return "Get the latest version of transaction on the blockchain"

    def execute(self, client, params):
        tx = client.get_latest_transaction_version()
        json_print_in_cmd({"latest_version": tx})


class TransactionCmdGetLatest(Command):
    def get_aliases(self):
        return ["latest", "l"]

    def get_description(self):
        return "Get the latest transaction"

    def execute(self, client, params):
        ver = client.get_latest_transaction_version()
        tx = client.get_transaction(ver)
        json_print_in_cmd(tx)
