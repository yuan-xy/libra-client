from libra_client.shell.libra_shell import *
from test_shell import prepare_shell, exec_input_with_client
from libra.account_address import Address
from libra.transaction import Script, TransactionPayload
from libra.account_address import Address
import libra
import libra_client
import pytest
import os
#import pdb

# try:
#     os.environ['TESTNET_LOCAL']
#     TESTNET_LOCAL = True
# except KeyError:
#     TESTNET_LOCAL = False
TESTNET_LOCAL = False

def test_move_compile_and_exec(capsys):
    if not TESTNET_LOCAL:
        return
    client, alias_to_cmd = prepare_shell(None)
    balance = client.grpc_client.get_balance("116998abbe30cb048b6c4d430922c9c2")
    exec_input_with_client("a r test/test.wallet", client, alias_to_cmd)
    exec_input_with_client("a mb 0 123", client, alias_to_cmd)
    exec_input_with_client("dev c 0 ../libra-client/test/pay_1.module.mvir module", client, alias_to_cmd)
    exec_input_with_client("dev p 0 ../libra-client/test/pay_1.module.mv", client, alias_to_cmd)
    exec_input_with_client("dev c 0 ../libra-client/test/use_pay.mvir script", client, alias_to_cmd)
    exec_input_with_client("dev e 0 ../libra-client/test/use_pay.mv  116998abbe30cb048b6c4d430922c9c2", client, alias_to_cmd)
    assert balance+1 == client.grpc_client.get_balance("116998abbe30cb048b6c4d430922c9c2")


def test_no_blob_of_non_exsits_address():
    if not TESTNET_LOCAL:
        return
    with pytest.raises(libra_client.client.AccountError):
        libra_client.Client("testnet").get_account_state(Address.random())

def test_create_account_and_rotate_key():
    if not TESTNET_LOCAL:
        return
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    c = libra_client.Client("testnet")
    wallet2 = libra_client.WalletLibrary.new()
    account = wallet2.new_account()
    address = account.address
    with pytest.raises(libra_client.client.AccountError):
        c.get_account_state(address)
    c.create_account(a0, address)
    account_resource = c.get_account_resource(address)
    assert account_resource.balance == 0
    assert account_resource.sequence_number == 0
    assert account_resource.sent_events.count == 0
    assert account_resource.received_events.count == 0
    assert Address.equal_address(account_resource.authentication_key, address)
    c.rotate_authentication_key(account, a0.public_key)
    account_resource = c.get_account_resource(address)
    assert account_resource.balance == 0
    assert account_resource.sequence_number == 1
    assert account_resource.sent_events.count == 0
    assert account_resource.received_events.count == 0
    assert bytes(account_resource.authentication_key) == a0.public_key
    # before rotate, authentication_key == address
    # after rotate,  authentication_key == public_key

def test_true_silent_cast_to_int_which_is_dangerous():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    wallet2 = libra_client.WalletLibrary.new()
    account = wallet2.new_account()
    script = Script.gen_create_account_script(account.address, account.auth_key_prefix)
    payload = TransactionPayload('Script', script)
    c = libra_client.Client("testnet")
    is_blocking=True
    with pytest.raises(TypeError):
        c.submit_payload(a0, payload, is_blocking)
        #is_blocking is acctual parsed as max_gas, and True is cast to 1.
        #so, error thrown: min gas required for txn: 600, gas submitted: 1



