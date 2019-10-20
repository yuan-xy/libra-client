#!/usr/bin/env python3
from datetime import datetime
import argparse
import sys, os, signal
import pdb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

import libra
from libra.version import version
from libra import Client, WalletLibrary
from libra.client import NETWORKS
from libra.cli.command import *
from libra.cli.account_cmds import AccountCmd
from libra.cli.transaction_cmds import TransactionCmd
from libra.cli.wallet_cmds import WalletCmd
from libra.cli.ledger_cmds import LedgerCmd
from libra.cli.color import set_force_color

TESTNET = NETWORKS['testnet']['host']

def get_commands(include_dev: bool):
    commands = [AccountCmd(), TransactionCmd(), WalletCmd(), LedgerCmd()]
    return get_commands_alias(commands)


def run_cmd(args):
    if args.color == 'always':
        set_force_color(True)
    if args.color == 'never':
        set_force_color(False)
    (commands, alias_to_cmd) = get_commands(args.host != TESTNET)
    if args.help or len(args.command) == 0:
        print_help(commands)
        return
    cmd = alias_to_cmd.get(args.command[0])
    if cmd is None:
        report_error(f"command `{args.command[0]}` does not exsits.")
        print_help(commands)
        return
    client = Client.new(args.host, args.port, args.validator_set_file, args.faucet_account_file)
    client.verbose = args.verbose
    #TODO: some cmd doesn't need client to be initialized.
    cmd.execute(client, args.command)


def get_parser():
    parser = argparse.ArgumentParser(prog='libra', add_help=False)
    parser.add_argument('-h', "--help", action='store_true', default=False)
    parser.add_argument('-a', "--host", default=TESTNET)
    parser.add_argument('-p', "--port", default=8000)
    parser.add_argument('-s', "--validator_set_file")
    parser.add_argument('-m', "--faucet_account_file")
    parser.add_argument('-v', "--verbose", action='store_true', default=False)
    parser.add_argument('-V', '--version', action='version', version=f'libra {version}')
    parser.add_argument('-c', '--color', choices=['always', 'auto', 'never'], default='auto')
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


def handler(signum, frame):
    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    parser = get_parser()
    argv = sys.argv[1:]
    if not sys.stdin.isatty():
        argv.extend(sys.stdin.read().strip().split())
    libra_args = parser.parse_args(argv)
    try:
        run_cmd(libra_args)
    except Exception as err:
        report_error("some error occured", err, libra_args.verbose)



if __name__ == '__main__':
    main()
