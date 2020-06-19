import libra
import libra_client
from libra_client.error import *
from libra import Address
from libra.transaction import *
from libra.contract_event import ContractEvent
from canoser import Uint64
import os
import pytest
import requests


def test_invalid_param():
    c = libra_client.Client("testnet")
    with pytest.raises(libra_client.LibraError) as excinfo:
        c.json_rpc("get_transactions", [])
    err = excinfo.value
    assert err.args[0]['error']['code']


def test_get_transaction():
    c = libra_client.Client("testnet")
    stx = c.get_transaction(1, True)
    assert stx.transaction.type == 'blockmetadata'
    assert stx.vm_status == 4001
    assert stx.success is True
    assert stx.gas_used == 600

def test_get_transactions3():
    c = libra_client.Client("testnet")
    start_version = 0
    txs = c.get_transactions(start_version, limit=3, include_events=True)
    assert len(txs) == 3
    for i, tx in enumerate(txs):
        assert i == tx.version
        assert tx.gas_used >= 0


def test_get_transaction_without_events():
    c = libra_client.Client("testnet")
    transactions = c.get_transactions(1, 1, False)
    assert len(transactions) == 1
    # assert hasattr(c, "latest_time") == True
    # assert c.latest_time > 1570_000_000_000_000


def test_get_tx_from_zero():
    c = libra_client.Client("testnet")
    transactions = c.get_transactions(0, 2, True)
    assert len(transactions) == 2


def test_get_tx_latest():
    c = libra_client.Client("testnet")
    ver = c.get_latest_transaction_version()
    if ver == 1:
        return
    transactions = c.get_transactions(ver-2, 2, True)
    assert len(transactions) == 2

def test_get_tx_zero():
    c = libra_client.Client("testnet")
    with pytest.raises(LibraError):
        c.get_transactions(1, 0, True)


def test_get_tx_invalid():
    c = libra_client.Client("testnet")
    with pytest.raises(LibraError):
        c.get_transactions(1, -1, True)

def test_get_latest_transaction_version():
    c = libra_client.Client("testnet")
    ver = c.get_latest_transaction_version()
    assert ver > 0

def test_get_balance():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    balance = c.get_balance(address)
    assert balance >= 0

def test_get_account_resource():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    ret = c.get_account_resource(address)
    assert len(ret.authentication_key) == 32*2 #hex
    assert ret.delegated_key_rotation_capability == False
    assert ret.delegated_withdrawal_capability == False
    assert len(ret.received_events_key) == libra.event.EVENT_KEY_LENGTH*2
    assert len(ret.sent_events_key) == libra.event.EVENT_KEY_LENGTH*2
    assert ret.sequence_number > 0
    balance = c.get_balance(address)
    assert balance >= 0
    addr = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nU\x0c\x18'
    assert addr == bytes.fromhex(address)
    ret2 = c.get_account_resource(addr)
    assert ret.delegated_withdrawal_capability == ret2.delegated_withdrawal_capability
    assert ret2.sequence_number >= ret.sequence_number


def test_account_not_exsits():
    address = "7af57fff206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e21"[:32]
    c = libra_client.Client("testnet")
    with pytest.raises(libra_client.client.AccountError):
        balance = c.get_account_state(address)

def test_get_account_transaction():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    txn = c.get_account_transaction(address, 0, True)
    if txn is None:
        return
    usecs = txn.transaction.expiration_time
    assert usecs//1000_000 > 1570_000_000

def test_get_account_transaction_non_exists():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    txn = c.get_account_transaction(address, Uint64.max_value, True)
    assert txn is None


def test_transfer_coin():
    wallet = libra_client.WalletLibrary.new()
    a0 = wallet.new_account()
    a1 = wallet.new_account()
    c = libra_client.Client("testnet")
    c.mint_coins(a0.address, a0.auth_key_prefix, 1234_000, is_blocking=True)
    balance0 = c.get_balance(a0.address, retry=True)
    c.create_account(a0, a1.address, a1.auth_key_prefix, is_blocking=True)
    balance1 = c.get_balance(a1.address, retry=True)
    ret = c.transfer_coin(a0, a1.address, 123, gas_unit_price=1, is_blocking=True)
    assert bytes(ret.raw_txn.sender) == a0.address
    assert ret.raw_txn.sequence_number == 0
    assert c.get_balance(a0.address) <= balance0 - 123
    assert c.get_balance(a1.address) == balance1 + 123

def test_client_init():
    client = libra_client.Client.new("localhost:8080")
    assert client.url == "localhost:8080"
    assert hasattr(client, "faucet_host") == False
    assert client.verbose == True
    assert client.faucet_account is not None


def test_client_testnet():
    c2 = libra_client.Client("testnet")
    if 'TESTNET_LOCAL' in os.environ:
        return
    assert c2.url == "https://client.testnet.libra.org"
    assert c2.verbose == True
    assert c2.faucet_account is None


def test_client_error():
    with pytest.raises(libra_client.client.LibraNetError):
        libra_client.Client("xnet")
    with pytest.raises(libra_client.client.LibraNetError):
        libra_client.Client("mainnet")
    with pytest.raises(FileNotFoundError):
        libra_client.Client.new("localhost:8000", "non_exsits_file")

def test_timeout():
    c = libra_client.Client("testnet")
    c.timeout = 0.001
    with pytest.raises(Exception) as excinfo:
        stx = c.get_transaction(1, True)
    error = excinfo.value
    assert "timeout" in error.__str__().lower() or "ConnectionError" in error.__str__()
