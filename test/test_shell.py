from libra.shell.libra_shell import *
from libra.account_address import gen_random_address
from tempfile import NamedTemporaryFile
import libra
import pytest
import os
#import pdb

try:
    os.environ['TESTNET_LOCAL']
    TESTNET_LOCAL = True
except KeyError:
    TESTNET_LOCAL = False


def test_shell():
    parser = get_parser()
    args = parser.parse_args("")
    assert args.host == "ac.testnet.libra.org"
    assert args.port == 0
    assert args.sync == False
    assert args.validator_set_file == None
    grpc_client = libra.Client.new(args.host, args.port, args.validator_set_file)
    assert TESTNET_LOCAL or hasattr(grpc_client, "faucet_host")


def test_recover_account_on_init(capsys):
    parser = get_parser()
    args = parser.parse_args("-n test/test.wallet -s libra/consensus_peers.config.toml".split())
    assert args.mnemonic_file == "test/test.wallet"
    assert args.validator_set_file == "libra/consensus_peers.config.toml"
    grpc_client = libra.Client.new(args.host, args.port, args.validator_set_file)
    client = ClientProxy(grpc_client, args)
    assert len(client.accounts) == 2


def prepare_shell(shell_args):
    parser = get_parser()
    if shell_args is None:
        shell_args = "-n test/test.wallet -s libra/consensus_peers.config.toml"
    args = parser.parse_args(shell_args.split())
    grpc_client = libra.Client.new(args.host, args.port, args.validator_set_file)
    client = ClientProxy(grpc_client, args)
    (_, alias_to_cmd) = get_commands(True)
    return (client, alias_to_cmd)

def exec_input(input, capsys, shell_args=None):
    (client, alias_to_cmd) = prepare_shell(shell_args)
    params = parse_cmd(input)
    cmd = alias_to_cmd.get(params[0])
    cmd.execute(client, params)
    #pdb.set_trace()
    return capsys.readouterr().out

def test_account_hint(capsys):
    output = exec_input("account", capsys, "")
    assert 'USAGE:' in output
    assert 'account <params>' in output

def test_account_create(capsys):
    output = exec_input("a create", capsys)
    #pdb.set_trace()
    assert 'Created/retrieved account' in output

def test_account_list(capsys):
    output = exec_input("account list", capsys, "")
    assert 'No user accounts' in output

def test_account_recover(capsys):
    output = exec_input("a r test/test.wallet", capsys, "")
    assert 'Wallet recovered and the first 2 child accounts were derived' in output
    assert '#0 address' in output
    assert '#1 address' in output

def test_account_write(capsys):
    tmp = NamedTemporaryFile('w+t')
    output = exec_input(f"a w {tmp.name}", capsys, "")
    assert 'Saved mnemonic seed to disk' in output
    tmp.close()

def test_account_create(capsys):
    output = exec_input("a m 0 123", capsys)
    assert 'Mint request submitted' in output

def test_query_hint(capsys):
    output = exec_input("query", capsys, "")
    assert 'USAGE:' in output
    assert 'query <params>' in output

def test_query_balance(capsys):
    output = exec_input("query b 0", capsys)
    assert 'Balance is:' in output

def test_query_seq(capsys):
    output = exec_input("query s 0", capsys)
    assert 'Sequence number is:' in output

def test_query_account_state(capsys):
    output = exec_input("query as 0", capsys)
    assert 'Latest account state is' in output

def test_query_txn_acc_seq(capsys):
    output = exec_input("query ts 0 0 false", capsys)
    assert 'Getting committed transaction by account and sequence number' in output

def test_query_transaction(capsys):
    output = exec_input("query txn_range 1 2 true", capsys)
    assert 'Transaction at version 1' in output
    assert 'Transaction at version 2' in output

def test_query_events(capsys):
    addr = libra.AccountConfig.association_address()
    output = exec_input(f"q ev {addr} sent 1 true 1", capsys, "")
    assert 'event_data' in output
    assert 'sequence_number: 1' in output

def test_transfer_coin(capsys):
    output = exec_input("t 0 1 123", capsys)
    assert 'Transaction submitted to validator' in output

def test_transfer_error(capsys):
    output = exec_input("t 0 1", capsys)
    assert 'transfer | transferb | t | tb' in output

def test_execute_script_on_testnet(capsys):
    client = libra.Client("testnet")
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    balance = client.get_balance(a0.address_hex)
    if balance <= 1:
        client.mint_coins(a0.address_hex, 9999999, True)
    addr1 = gen_random_address()
    output = exec_input(f"dev e 0 transaction_scripts/peer_to_peer_transfer.mv {addr1} 1", capsys)
    assert 'Compiling program' in output
    if TESTNET_LOCAL:
        assert "code: InvalidUpdate" in output
        assert "Failed to update gas price to 0" in output
    else:
        seq = client.get_sequence_number(a0.address_hex)
        client.wait_for_transaction(a0.address_hex, seq-1)
        balance2 = client.get_balance(addr1)
        if balance2 == 0:
            tx, _ = client.get_account_transaction_proto(a0.address_hex, seq-1)
            #TODO: Under what conditions this transaction will fail
            print(tx.proof.transaction_info.major_status)
        else:
            assert balance2 == 1


def test_publish_module_to_testnet(capsys):
    output = exec_input(f"dev p 0 transaction_scripts/peer_to_peer_transfer.mv", capsys)
    assert "ERROR" in output
    if TESTNET_LOCAL:
        assert 'Publish move module on-chain: (3001' in output
    else:
        assert 'Publish move module on-chain: (12' in output

def test_faucet_key_no_host(capsys):
    with pytest.raises(ValueError):
        prepare_shell("-m libra/faucet_key_for_test")

def test_faucet_key_with_host(capsys):
    args = "-m libra/faucet_key_for_test -a localhost -s libra/consensus_peers.config.toml"
    client, _ = prepare_shell(args)
    assert client.faucet_account


def exec_input_with_client(input, client, alias_to_cmd):
    params = parse_cmd(input)
    cmd = alias_to_cmd.get(params[0])
    cmd.execute(client, params)
