from libra.cli.command import *

class AccountCommand(Command):
    def get_aliases(self):
        return ["account", "a"]

    def get_description(self):
        return "Account operations"

    def execute(self, client, params):
        commands = [
            AccountCommandCreate(),
            AccountCommandListAccounts(),
            AccountCommandRecoverWallet(),
            AccountCommandWriteRecovery(),
            AccountCommandMint()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class AccountCommandCreate(Command):
    def get_aliases(self):
        return ["create", "c"]

    def get_description(self):
        return "Create an account. Returns reference ID to use in other operations"

    def execute(self, client, params):
        print(">> Creating/retrieving next account from wallet")
        index, account = client.create_next_account()
        print(
            "Created/retrieved account #{} address {}".format(
                index,
                account.address.hex()
            )
        )


class AccountCommandListAccounts(Command):
    def get_aliases(self):
        return ["list", "la"]

    def get_description(self):
        return "Print all accounts that were created or loaded"

    def execute(self, client, params):
        client.print_all_accounts()


class AccountCommandRecoverWallet(Command):
    def get_aliases(self):
        return ["recover", "r"]

    def get_params_help(self):
        return "<file_path>"

    def get_description(self):
        return "Recover Libra wallet from the file path"

    def execute(self, client, params):
        print(">> Recovering Wallet")
        accounts = client.recover_wallet_accounts(params[1])
        print(f"Wallet recovered and the first {len(accounts)} child accounts were derived")
        for index, data in enumerate(accounts):
            print("#{} address {}".format(index, data.address.hex()))


class AccountCommandWriteRecovery(Command):
    def get_aliases(self):
        return ["write", "w"]

    def get_params_help(self):
        return "<file_path>"

    def get_description(self):
        return "Save Libra wallet mnemonic recovery seed to disk"

    def execute(self, client, params):
        print(">> Saving Libra wallet mnemonic recovery seed to disk")
        client.write_recovery(params[1])
        print("Saved mnemonic seed to disk")


class AccountCommandMint(Command):
    def get_aliases(self):
        return ["mint", "mintb", "m", "mb"]

    def get_params_help(self):
        return "<receiver_account_ref_id>|<receiver_account_address> <number_of_coins>"

    def get_description(self):
        return "Mint coins to the account. Suffix 'b' is for blocking"

    def execute(self, client, params):
        print(">> Minting coins")
        is_blocking = blocking_cmd(params[0])
        client.mint_coins(params[1], params[2], is_blocking)
        if is_blocking:
            print("Finished minting!")
        else:
            print("Mint request submitted")
