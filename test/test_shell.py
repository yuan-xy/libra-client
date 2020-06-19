from libra_client.shell.libra_shell import *
from libra.account_address import Address
from tempfile import NamedTemporaryFile
import libra
import libra_client
import pytest
import os
import traceback

try:
    os.environ['TESTNET_LOCAL']
    TESTNET_LOCAL = True
except KeyError:
    TESTNET_LOCAL = False


def test_shell():
    parser = get_parser()
    args = parser.parse_args("")
    assert args.url == "https://client.testnet.libra.org"
    assert args.sync == False
    grpc_client = libra_client.Client.new(args.url)
    assert TESTNET_LOCAL or hasattr(grpc_client, "faucet_host")


def test_recover_account_on_init(capsys):
    parser = get_parser()
    args = parser.parse_args("-n test/test.wallet".split())
    assert args.mnemonic_file == "test/test.wallet"
    grpc_client = libra_client.Client.new(args.url)
    client = ClientProxy(grpc_client, args)
    assert len(client.accounts) == 2


def prepare_shell(shell_args):
    parser = get_parser()
    if shell_args is None:
        shell_args = "-n test/test.wallet"
    args = parser.parse_args(shell_args.split())
    args.verbose = True
    grpc_client = libra_client.Client.new(args.url)
    client = ClientProxy(grpc_client, args)
    (_, alias_to_cmd) = get_commands(True)
    return (client, alias_to_cmd)

def exec_input(input, capsys, shell_args=None):
    (client, alias_to_cmd) = prepare_shell(shell_args)
    params = parse_cmd(input)
    cmd = alias_to_cmd.get(params[0])
    cmd.execute(client, params)
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

def test_mint_account(capsys):
    output = exec_input("a m 0 123", capsys)
    assert 'Error' not in output
    assert 'Mint' in output

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
    addr = libra.AccountConfig.treasury_compliance_account_address()
    output = exec_input(f"q ev {addr} sent 1 true 1", capsys, "")
    assert 'data' in output
    assert "'sequence_number': 1" in output

def test_transfer_coin(capsys):
    try:
        output = exec_input("t 0 1 123", capsys)
        assert 'Transaction submitted to validator' in output
    except libra_client.error.LibraError:
        pass

def test_transfer_error(capsys):
    output = exec_input("t 0 1", capsys)
    assert 'transfer | transferb | t | tb' in output

def test_execute_script_on_testnet(capsys):
    if TESTNET_LOCAL:
        #TODO: why should sleep some seconds to avoid MempoolError
        import time
        time.sleep(1)
    client = libra_client.Client("testnet")
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    balance = client.get_balance(a0.address_hex)
    if balance <= 1:
        try:
            client.mint_coins(a0.address_hex, a0.auth_key_prefix, 9999999, True)
        except Exception:
            params = {
                "receiver_account_address": a0.address_hex,
                "number_of_micro_libra": 9
            }
            import requests
            requests.post("http://apitest.moveonlibra.com/v1/transactions/mint_mol", data=params)
    addr1 = wallet.accounts[1].address.hex()
    addr1_prefix = 'b"'+wallet.accounts[1].auth_key_prefix.hex()+'"'
    output = exec_input(f"dev e 0 test/peer_to_peer.mv {addr1} {addr1_prefix} 1", capsys)
    assert 'Compiling program' in output
    return #TODO: peer_to_peer need type parameter which is not support in libra shell.

    if TESTNET_LOCAL:
        if "MempoolError" in output:
            pass
            # assert "Failed to update gas price to 0" in output
        else:
            assert "Successfully finished execution" in output
    else:
        seq = client.get_sequence_number(a0.address_hex)
        #should get seq by submited transaction, above will get error seq in concurrent env.
        client.wait_for_transaction(a0.address_hex, seq-1)
        balance2 = client.get_balance(addr1)
        assert balance2 >= 0


def test_publish_module_to_testnet(capsys):
    output = exec_input(f"dev p 0 test/peer_to_peer.mv", capsys)
    assert 'Publish move module on-chain: ' in output
    assert "ERROR" in output


def test_faucet_key_no_host(capsys):
    with pytest.raises(ValueError):
        prepare_shell("-m libra/mint.key")

def test_faucet_key_with_host(capsys):
    args = "-m libra/mint.key -u localhost"
    client, _ = prepare_shell(args)
    assert client.faucet_account


def exec_input_with_client(input, client, alias_to_cmd):
    params = parse_cmd(input)
    cmd = alias_to_cmd.get(params[0])
    cmd.execute(client, params)

def test_ledger_time(capsys):
    # output = exec_input("ledger time", capsys)
    from libra_client.cli.ledger_cmds import LedgerCmdTime
    client = libra_client.Client("testnet")
    LedgerCmdTime().execute(client, {})
    output = capsys.readouterr().out
    assert 'start_time' in output
    assert 'latest_time' in output