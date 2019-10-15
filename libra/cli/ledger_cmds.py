from libra.cli.command import *
from libra.wallet_library import WalletLibrary
from libra.json_print import json_print
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
        json_print(info)


class LedgerCmdTime(Command):
    def get_aliases(self):
        return ["time", "t"]

    def get_description(self):
        return "Get the latest ledger time of Libra blockchain"

    def execute(self, client, params):
        info = client.get_latest_ledger_info()
        second = info.timestamp_usecs / 1000_000
        dt = datetime.fromtimestamp(info.timestamp_usecs / 1000_000)
        json_print({"time": dt.strftime("%Y-%m-%dT%H:%M:%S")})