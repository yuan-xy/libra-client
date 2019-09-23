from command import *

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
        subcommand_execute(params[0], commands, client, params[1:])


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
        if len(params) != 2:
            print("Invalid number of arguments for recovering wallets")
            return
        print(">> Recovering Wallet")
        try:
            accounts = client.recover_wallet_accounts(params[1])
            print(f"Wallet recovered and the first {len(accounts)} child accounts were derived")
            for index, data in enumerate(accounts):
                print("#{} address {}".format(index, data.address.hex()))
        except Exception as err:
            report_error("Error recovering Libra wallet", err)


class AccountCommandWriteRecovery(Command):
    def get_aliases(self):
        return ["write", "w"]

    def get_params_help(self):
        return "<file_path>"

    def get_description(self):
        return "Save Libra wallet mnemonic recovery seed to disk"

    def execute(self, client, params):
        if len(params) != 2:
            print("Invalid number of arguments for writing recovery wallets")
            return
        print(">> Saving Libra wallet mnemonic recovery seed to disk")
        try:
            client.write_recovery(params[1])
            print("Saved mnemonic seed to disk")
        except Exception as err:
            report_error("Error writing mnemonic recovery seed to file", err)


class AccountCommandMint(Command):
    def get_aliases(self):
        return ["mint", "mintb", "m", "mb"]

    def get_params_help(self):
        return "<receiver_account_ref_id>|<receiver_account_address> <number_of_coins>"

    def get_description(self):
        return "Mint coins to the account. Suffix 'b' is for blocking"

    def execute(self, client, params):
        if len(params) != 3:
            print("Invalid number of arguments for mint")
            return
        if not hasattr(client.grpc_client, "faucet_host"):
            print("Doesn't support mint on dev net.")
            return
        print(">> Minting coins")
        is_blocking = blocking_cmd(params[0])
        client.mint_coins(params[1], params[2], is_blocking)
        if is_blocking:
            print("Finished minting!")
        else:
            print("Mint request submitted")
        #report_error("Error minting coins", e),
