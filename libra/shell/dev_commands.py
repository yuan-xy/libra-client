from libra.cli.command import *
from libra.bytecode import get_code_by_filename

class DevCommand(Command):
    def get_aliases(self):
        return ["dev"]

    def get_description(self):
        return "Local move development"

    def get_notice(self):
        return "Libra project should exsits in '../libra', as a parallel dir to libra-client project"

    def execute(self, client, params):
        commands = [
            DevCommandCompile(),
            DevCommandPublish(),
            DevCommandExecute()
        ]
        self.subcommand_execute(params[0], commands, client, params[1:])


class DevCommandCompile(Command):
    def get_aliases(self):
        return ["compile", "c"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <file_path> <module|script> [output_file_path (compile into tmp file by default)]"

    def get_description(self):
        return "Compile move program"

    def execute(self, client, params):
        print(">> Compiling program");
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

    def execute(self, client, params):
        print(">> Compiling program");
        client.publish_module(params[1], params[2])
        print("Successfully published module")


class DevCommandExecute(Command):
    def get_aliases(self):
        return ["execute", "e"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <compiled_module_path> [parameters ...]"

    def get_description(self):
        return "Execute custom move script"

    def execute(self, client, params):
        print(">> Compiling program")
        client.execute_script(params[1], params[2], params[3:])
        print("Successfully finished execution")

