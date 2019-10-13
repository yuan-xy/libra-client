import abc
import sys
import os
import traceback
from color import print_color


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


def report_error(msg, err, verbose):
    print(f"[ERROR] {msg}: {err}")
    if verbose:
        traceback.print_exc()

def parse_cmd(cmd_str: str):
    return cmd_str.split()

def parse_bool(para_str):
    para = para_str.lower()
    if para == "true" or para == "t":
        return True
    elif para == "false" or para == "f":
        return False
    else:
        raise IOError(f"Unknown support bool str: {para_str}")

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
    print_commands(commands)

def print_commands(commands):
    for cmd in commands:
        print_color(" | ".join(cmd.get_aliases()), bcolors.OKGREEN, end='')
        print_color(" " + cmd.get_params_help(), bcolors.OKBLUE)
        print("\t" + cmd.get_description())

def blocking_cmd(cmd: str) -> bool:
    return cmd.endswith('b')


def debug_format_cmd(cmd: str) -> bool:
    return cmd.endswith('?')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
