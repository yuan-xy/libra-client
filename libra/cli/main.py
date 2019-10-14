#!/usr/bin/env python3
from datetime import datetime
import argparse
import sys
import os
import pdb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

import libra
from libra.version import version
from libra import Client, WalletLibrary
from libra.cli.command import *
from libra.cli.account_cmds import AccountCmd
from libra.cli.transaction_cmds import TransactionCmd
from libra.cli.color import support_color


def get_commands(include_dev: bool):
    commands = [AccountCmd(), TransactionCmd()]
    alias_to_cmd = {}
    for command in commands:
        for alias in command.get_aliases():
            alias_to_cmd[alias] = command
    return (commands, alias_to_cmd)


def run_cmd(parser, args):
    client_info = f"Connected to validator at: {args.host}:{args.port}"
    (commands, alias_to_cmd) = get_commands(args.faucet_account_file)
    if args.help:
        parser.print_help()
        print("\nUse the following commands:\n")
        print_commands(commands)
        return
    client = Client.new(args.host, args.port, args.validator_set_file)
    params = args.command
    cmd = alias_to_cmd.get(params[0])
    #pdb.set_trace()
    if cmd is not None:
        cmd.execute(client, params)


def get_parser():
    parser = argparse.ArgumentParser(prog='libra', add_help=False)
    parser.add_argument('-h', "--help", action='store_true', default=False, help='Show help message.')
    parser.add_argument('-a', "--host", default="ac.testnet.libra.org", help='Host address/name to connect to')
    parser.add_argument('-p', "--port", default=8000, help='Admission Control port to connect to. [default: 8000]')
    parser.add_argument('-s', "--validator_set_file", help='File location from which to load config of trusted validators.')
    parser.add_argument('-m', "--faucet_account_file", help='Path to the generated keypair for the faucet account.')
    parser.add_argument('-v', "--verbose", action='store_true', default=False, help='Verbose output.')
    parser.add_argument('-V', '--version', action='version', version=f'libra {version}')
    parser.add_argument('command', nargs='*', help='command such as account/wallet/transaction/ledger/event etc.')
    return parser

def main():
    parser = get_parser()
    libra_args = parser.parse_args(sys.argv[1:])
    run_cmd(parser, libra_args)
    #pdb.set_trace()


if __name__ == '__main__':
    main()
