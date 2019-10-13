from command import *
from libra.bytecode import get_code_by_filename

class DevCommand(Command):
    def get_aliases(self):
        return ["dev"]

    def get_description(self):
        return "Local move development"

    def execute(self, client, params):
        commands = [
            # DevCommandCompile(),
            DevCommandPublish(),
            DevCommandExecute()
        ]
        subcommand_execute(params[0], commands, client, params[1:])


class DevCommandCompile(Command):
    def get_aliases(self):
        return ["compile", "c"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <file_path> <module|script> [output_file_path (compile into tmp file by default)]"

    def get_description(self):
        return "Compile move program"

    def execute(self, client, params):
        if len(params) < 4 or len(params) > 5:
            print("Invalid number of arguments for compilation")
            return
        try:
            print(">> Compiling program");
            path = client.compile_program(params)
            print(f"Successfully compiled a program at {path}")
        except Exception as err:
            report_error("Failed to compiled a program", err, client.verbose)


class DevCommandPublish(Command):
    def get_aliases(self):
        return ["publish", "p"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <compiled_module_path>"

    def get_description(self):
        return "Publish move module on-chain"

    def execute(self, client, params):
        if len(params) != 3:
            print("Invalid number of arguments to publish module")
            return
        try:
            print(">> Compiling program");
            client.publish_module(params[1], params[2])
            print("Successfully published module")
        except Exception as err:
            report_error("Failed to published module", err, client.verbose)


class DevCommandExecute(Command):
    def get_aliases(self):
        return ["execute", "e"]

    def get_params_help(self):
        return "<sender_account_address>|<sender_account_ref_id> <compiled_module_path> [parameters]"

    def get_description(self):
        return "Execute custom move script"

    def execute(self, client, params):
        if len(params) < 3:
            print("Invalid number of arguments to execute script")
            return
        try:
            print(">> Compiling program")
            client.execute_script(params[1], params[2], params[3:])
            print("Successfully finished execution")
        except Exception as err:
            report_error("Failed to execute", err, client.verbose)

