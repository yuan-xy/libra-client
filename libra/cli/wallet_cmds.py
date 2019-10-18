from libra.cli.command import *
from libra.wallet_library import WalletLibrary
from libra.json_print import to_json_serializable


class WalletCmd(Command):
    def get_aliases(self):
        return ["wallet", "w"]

    def get_description(self):
        return "show account information of a wallet derived from mnemonic file"

    def execute(self, client, params):
        commands = [
            WalletCmdShow(),
            WalletCmdAccount(),
            WalletCmdBalance(),
            WalletCmdCreate(),
            WalletCmdCreateNewAccount()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class WalletCmdShow(Command):
    def get_aliases(self):
        return ["show", "s"]

    def get_params_help(self):
        return "<mnemonic_file_path>"

    def get_description(self):
        return "Show the mnemonic words, seed and addresses of a wallet"

    def execute(self, client, params):
        wallet = WalletLibrary.recover(params[1])
        json_print_in_cmd(wallet)


class WalletCmdAccount(Command):
    def get_aliases(self):
        return ["accounts", "a"]

    def get_params_help(self):
        return "<mnemonic_file_path>"

    def get_description(self):
        return "Show the keypair and address of accounts in a wallet"

    def execute(self, client, params):
        wallet = WalletLibrary.recover(params[1])
        arr = []
        for index, account in enumerate(wallet.accounts):
            amap = to_json_serializable(account)
            amap["index"] = index
            arr.append(amap)
        json_print_in_cmd(arr)




class WalletCmdBalance(Command):
    def get_aliases(self):
        return ["balance", "b"]

    def get_params_help(self):
        return "<mnemonic_file_path>"

    def get_description(self):
        return "Get the balance of all accounts in a wallet"

    def execute(self, client, params):
        wallet = WalletLibrary.recover(params[1])
        maps = {}
        for account in wallet.accounts:
            maps[account.address_hex] = client.get_balance(account.address_hex)
            #TODO: multi query combine to one
        maps["total_balance"] = sum(maps.values())
        json_print_in_cmd(maps)


class WalletCmdCreate(Command):
    def get_aliases(self):
        return ["create_wallet", "cw"]

    def get_params_help(self):
        return "<mnemonic_file_path>"

    def get_description(self):
        return "create a new wallet and save the mnemonic file to <mnemonic_file_path>"

    def execute(self, client, params):
        wallet = WalletLibrary.new()
        wallet.write_recovery(params[1])
        jobj = to_json_serializable(wallet)
        jobj["file_save_to"] = params[1]
        json_print_in_cmd(jobj)


class WalletCmdCreateNewAccount(Command):
    def get_aliases(self):
        return ["create_account", "ca"]

    def get_params_help(self):
        return "<creator_id> <mnemonic_file_path>"

    def get_description(self):
        return "Create new account by exsiting account and sync to the wallet's mnemonic file."

    def execute(self, client, params):
        wfile = params[2]
        wallet = WalletLibrary.recover(wfile)
        sender_account = wallet.get_account_by_address_or_refid(params[1])
        fresh_address = wallet.new_account().address
        resp = client.create_account(sender_account, fresh_address)
        wallet.write_recovery(wfile)
        json_print_in_cmd({"new_account_address": fresh_address})
