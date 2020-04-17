from libra_client.cli.command import Command
from libra.waypoint import Waypoint


class DevCommand(Command):
    def get_aliases(self):
        return ["dev"]

    def get_description(self):
        return "Local move development"

    def get_notice(self):
        return "Libra project should exsits in '../libra', as a parallel dir to libra-client project"

    def execute(self, client, params, **kwargs):
        commands = [
            DevCommandCompile(),
            DevCommandPublish(),
            DevCommandExecute(),
            DevCommandAddValidator(),
            DevCommandRemoveValidator(),
            DevCommandRegisterValidator(),
            DevCommandGenWaypoint()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:], **kwargs)


class DevCommandCompile(Command):
    def get_aliases(self):
        return ["compile", "c"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <file_path> <module|script> [output_file_path (compile into tmp file by default)]"

    def get_description(self):
        return "Compile move program"

    def execute(self, client, params, **kwargs):
        print(">> Compiling program")
        file_path = params[2]
        if params[3] == "module":
            is_module = True
        elif params[3] == "script":
            is_module = False
        else:
            raise TypeError(f"{params[3]} is illegal.")
        path = client.compile_program(params[1], file_path, is_module, params[4:])
        print(f"Successfully compiled a program at {path}")


class DevCommandPublish(Command):
    def get_aliases(self):
        return ["publish", "p"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <compiled_module_path>"

    def get_description(self):
        return "Publish move module on-chain"

    def execute(self, client, params, **kwargs):
        print(">> Compiling program")
        client.publish_module(params[1], params[2])
        print("Successfully published module")


class DevCommandExecute(Command):
    def get_aliases(self):
        return ["execute", "e"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <compiled_module_path> [parameters ...]"

    def get_description(self):
        return "Execute custom move script"

    def execute(self, client, params, **kwargs):
        print(">> Compiling program")
        client.execute_script(params[1], params[2], params[3:])
        print("Successfully finished execution")


class DevCommandAddValidator(Command):
    def get_aliases(self):
        return ["add_validator"]

    def get_params_help(self):
        return "<validator_account_address>"

    def get_description(self):
        return "Add an account address to the validator set"

    def execute(self, client, params, **kwargs):
        client.grpc_client.add_validator_with_faucet_account(params[1])
        print("Successfully finished execution")


class DevCommandRemoveValidator(Command):
    def get_aliases(self):
        return ["remove_validator"]

    def get_params_help(self):
        return "<validator_account_address>"

    def get_description(self):
        return "Remove an existing account address from the validator set"

    def execute(self, client, params, **kwargs):
        client.grpc_client.remove_validator_with_faucet_account(params[1])
        print("Successfully finished execution")


class DevCommandRegisterValidator(Command):
    def get_aliases(self):
        return ["register_validator"]

    def get_params_help(self):
        return "<consensus_pubkey> <validator_network_signing_pubkey> <validator_network_identity_pubkey> <validator_network_address> <fullnodes_network_identity_pubkey> <fullnodes_network_address>"

    def get_description(self):
        return "Register an validator candidate"

    def execute(self, client, params, **kwargs):
        client.grpc_client.register_validator_with_faucet_account(params[1], params[2], params[3], params[4], params[5], params[6])
        print("Successfully finished execution")


class DevCommandGenWaypoint(Command):
    def get_aliases(self):
        return ["gen_waypoint"]

    def get_params_help(self):
        return ""

    def get_description(self):
        return "Generate a waypoint for the latest epoch change LedgerInfo"

    def execute(self, client, params, **kwargs):
        print("Retrieving the uptodate ledger info...")
        client.grpc_client.get_latest_ledger_info()
        latest_epoch_change_li = client.grpc_client.state.latest_epoch_change_li
        if latest_epoch_change_li is None:
            print("No epoch change LedgerInfo found")
            return
        waypoint = Waypoint.new(latest_epoch_change_li.ledger_info)
        print("Waypoint (end of epoch {}, time {}): {}".format(
            latest_epoch_change_li.ledger_info.epoch,
            latest_epoch_change_li.ledger_info.timestamp_usecs,
            waypoint
        )
        )
