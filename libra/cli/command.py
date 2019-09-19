import abc

class Command(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def get_aliases(self):
        pass

    def get_params_help(self):
        return ""

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def execute(self, client, params):
        pass


def report_error(msg, err):
    print(f"[ERROR] {msg}: {err}")

def parse_cmd(cmd_str: str):
    return cmd_str.split()


def subcommand_execute(parent_command_name, commands, client, params):
    if len(params) == 0:
        print_subcommand_help(parent_command_name, commands)
        return
    commands_map = {}
    for i, cmd in enumerate(commands):
        for alias in cmd.get_aliases():
            if commands_map.__contains__(alias):
                raise AssertionError(f"Duplicate alias {alias}")
            commands_map[alias] = i
    idx = commands_map.get(params[0])
    if idx is not None:
        commands[idx].execute(client, params)
    else:
        print_subcommand_help(parent_command_name, commands)


def print_subcommand_help(parent_command, commands):
    print(f"usage: {parent_command} <arg>\n\nUse the following args for this command:\n")
    for cmd in commands:
        print(
            "{} {}\n\t{}".format(
                " | ".join(cmd.get_aliases()),
                cmd.get_params_help(),
                cmd.get_description()
            )
        )
    print("\n")


def blocking_cmd(cmd: str) -> bool:
    return cmd.endswith('b')


def debug_format_cmd(cmd: str) -> bool:
    return cmd.endswith('?')
