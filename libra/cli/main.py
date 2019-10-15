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
from libra.cli.wallet_cmds import WalletCmd
from libra.cli.ledger_cmds import LedgerCmd
from libra.cli.color import support_color


def get_commands(include_dev: bool):
    commands = [AccountCmd(), TransactionCmd(), WalletCmd(), LedgerCmd()]
    return get_commands_alias(commands)


def run_cmd(parser, args):
    (commands, alias_to_cmd) = get_commands(args.faucet_account_file)
    if args.help or len(args.command) == 0:
        print_help(commands)
        return
    client = Client.new(args.host, args.port, args.validator_set_file)
    client.verbose = args.verbose #bad smell
    params = args.command
    cmd = alias_to_cmd.get(params[0])
    #pdb.set_trace()
    if cmd is not None:
        cmd.execute(client, params)


def get_parser():
    parser = argparse.ArgumentParser(prog='libra', add_help=False)
    parser.add_argument('-h', "--help", action='store_true', default=False)
    parser.add_argument('-a', "--host", default="ac.testnet.libra.org")
    parser.add_argument('-p', "--port", default=8000)
    parser.add_argument('-s', "--validator_set_file")
    parser.add_argument('-m', "--faucet_account_file")
    parser.add_argument('-v', "--verbose", action='store_true', default=False)
    parser.add_argument('-V', '--version', action='version', version=f'libra {version}')
    parser.add_argument('command', nargs='*')
    return parser

def print_help(commands):
    print("USAGE: ")
    print_color("\tlibra", bcolors.OKGREEN, end='')
    print_color(" [options]", bcolors.OKBLUE, end='')
    print_color(" command", bcolors.OKGREEN, end='')
    print_color(" [command parameters ...]", bcolors.OKBLUE)
    print("\nOptional arguments:\n")
    print_color(" -a | --host", bcolors.OKBLUE, end='')
    print(" HOST  Host address/name to connect to.", end='')
    print_color(" [default:testnet]", bcolors.WARNING)
    print_color(" -p | --port", bcolors.OKBLUE, end='')
    print(" PORT  Admission Control port to connect to.", end='')
    print_color(" [default: 8000]", bcolors.WARNING)
    print_color(" -s | --validator_set_file", bcolors.OKBLUE, end='')
    print("\n\t    File location from which to load config of trusted validators.")
    print_color(" -v | --verbose", bcolors.OKBLUE, end='')
    print(" Verbose output")
    print_color(" -V | --version", bcolors.OKBLUE, end='')
    print(" Show program's version number and exit")
    print_color(" -h | --help", bcolors.OKBLUE, end='')
    print(" Show this help message and exit")
    print("\nUse the following commands:\n")
    print_commands(commands)
    print("")




def main():
    parser = get_parser()
    libra_args = parser.parse_args(sys.argv[1:])
    run_cmd(parser, libra_args)
    #pdb.set_trace()


if __name__ == '__main__':
    main()
