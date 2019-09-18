#!/usr/bin/env python3

import argparse
import sys
import os
import pdb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from libra import Client
from command import *
from account_commands import AccountCommand
from query_commands import QueryCommand
from transfer_commands import TransferCommand
from dev_commands import DevCommand


def get_commands(include_dev: bool):
    commands = [AccountCommand(), QueryCommand(), TransferCommand()]
    if include_dev:
        commands.append(DevCommand())
    alias_to_cmd = {}
    for command in commands:
        for alias in command.get_aliases():
            alias_to_cmd[alias] = command
    return (commands, alias_to_cmd)


def run_shell(libra_args):
    client = Client("testnet")
    client_info = "Connected to validator at: {}:{}".format(libra_args.host, libra_args.port)
    (commands, alias_to_cmd) = get_commands(False)
    while True:
        line = input('libra% ')
        params = parse_cmd(line)
        if len(params) == 0:
            continue
        cmd = alias_to_cmd.get(params[0])
        if cmd is not None:
            cmd.execute(client, params)
        else:
            if params[0] == "quit" or params[0] == "q!":
                break
            elif params[0] == "help" or params[0] == "h":
                print_help(client_info, commands)
            else:
                print(f"Unknown command: {params[0]}")


def print_help(client_info: str, commands):
    print(client_info)
    print("usage: <command> <args>\n\nUse the following commands:\n")
    for cmd in commands:
        print(
            "{} {}\n\t{}".format(
            " | ".join(cmd.get_aliases()),
            cmd.get_params_help(),
            cmd.get_description()
            )
        )
    print("help | h \n\tPrints this help")
    print("quit | q! \n\tExit this client")
    print("\n")


def main():
    parser = argparse.ArgumentParser(prog='libra-shell')
    parser.add_argument('-a', "--host", help='Host address/name to connect to')
    parser.add_argument('-p', "--port", help='Admission Control port to connect to. [default: 8000]')
    #parser.print_help()
    AccountCommand()
    libra_args = parser.parse_args(sys.argv[1:])
    run_shell(libra_args)



if __name__ == '__main__':
    main()
