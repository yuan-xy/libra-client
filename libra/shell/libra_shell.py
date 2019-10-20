#!/usr/bin/env python3
from datetime import datetime
import argparse
import sys, os, signal

if os.name == 'posix':
    import readline

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './')))

from libra.version import version
from libra import Client, WalletLibrary
from libra.cli.command import *
from account_commands import AccountCommand
from query_commands import QueryCommand
from transfer_commands import TransferCommand
from dev_commands import DevCommand
from client_proxy import ClientProxy
from libra.cli.color import support_color, print_color


def get_commands(include_dev: bool):
    commands = [AccountCommand(), QueryCommand(), TransferCommand()]
    if include_dev:
        commands.append(DevCommand())
    return get_commands_alias(commands)


def run_shell(args):
    grpc_client = Client.new(args.host, args.port, args.validator_set_file, args.faucet_account_file)
    try:
        grpc_client.get_latest_transaction_version()
    except Exception as err:
        report_error(f"Not able to connect to validator at {args.host}:{args.port}", err, args.verbose)
        return
    client = ClientProxy(grpc_client, args)
    client_info = f"Connected to validator at: {args.host}:{args.port}"
    print(client_info)
    (commands, alias_to_cmd) = get_commands(grpc_client.faucet_account is not None)
    while True:
        prompt = "libra% "
        if support_color():
            prompt = f'\033[91m{prompt}\033[0m'
        try:
            line = input(prompt)
        except EOFError:
            sys.exit(0)
        params = parse_cmd(line)
        if len(params) == 0:
            continue
        cmd = alias_to_cmd.get(params[0])
        if cmd is not None:
            if args.verbose:
                print(datetime.now().strftime("%Y-%m-%d,%H:%M:%S"))
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
    print_commands(commands)
    print_color("help | h", bcolors.OKGREEN)
    print("\tPrints this help")
    print_color("quit | q!", bcolors.OKGREEN)
    print("\tExit this client")
    print("\n")

def get_parser():
    parser = argparse.ArgumentParser(prog='libra-shell')
    parser.add_argument('-a', "--host", default="ac.testnet.libra.org", help='Host address/name to connect to')
    parser.add_argument('-p', "--port", default=8000, help='Admission Control port to connect to. [default: 8000]')
    parser.add_argument('-r', "--sync", action='store_true', default=False, help='If set, client will sync with validator during wallet recovery.')
    parser.add_argument('-s', "--validator_set_file", help='File location from which to load config of trusted validators.')
    parser.add_argument('-n', "--mnemonic_file", help='File location from which to load mnemonic word for user account address/key generation.')
    parser.add_argument('-m', "--faucet_account_file", help='Path to the generated keypair for the faucet account.')
    parser.add_argument('-v', "--verbose", action='store_true', default=False, help='Verbose output.')
    parser.add_argument('-V', '--version', action='version', version=f'libra-client {version}')
    return parser


def handler(signum, frame):
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    #signal.signal(signal.SIGTSTP, handler)
    if os.name == 'posix':
        readline.set_history_length(1000)
    parser = get_parser()
    libra_args = parser.parse_args(sys.argv[1:])
    try:
        run_shell(libra_args)
    except Exception as err:
        report_error("some error occured", err, libra_args.verbose)


if __name__ == '__main__':
    main()
