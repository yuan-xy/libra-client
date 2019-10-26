import libra
from libra.transaction import *

import pytest
import pdb

def test_events():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    #pdb.set_trace()
    assert len(events) == 2

def test_get_transaction():
    c = libra.Client("testnet")
    stx = c.get_transaction(1)
    assert bytes(stx.raw_txn.sender).hex() == libra.AccountConfig.association_address()
    assert stx.raw_txn.sequence_number == 1
    assert stx.raw_txn.payload.index == 2
    assert stx.raw_txn.payload.Script == True
    assert stx.raw_txn.payload.value.code == Script.get_script_bytecode("mint")
    assert stx.raw_txn.payload.value.args[0].index == 1
    assert stx.raw_txn.payload.value.args[0].Address == True
    assert stx.raw_txn.payload.value.args[1].index == 0
    assert stx.raw_txn.payload.value.args[1].U64 == True
    assert stx.raw_txn.payload.value.args[1].value == 250000000
    assert stx.raw_txn.max_gas_amount == 140000
    assert stx.raw_txn.gas_unit_price == 0
    assert stx.raw_txn.expiration_time > 1_568_000_000
    assert stx.raw_txn.expiration_time < 11_568_000_000
    assert len(stx.public_key) == 32
    assert len(stx.signature) == 64
    stx.check_signature
    stx.__str__()

def test_get_tx_with_events():
    c = libra.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(1, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2

def test_get_tx_from_zero():
    c = libra.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(0, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2
    transactions, events_for_versions = c.get_transactions_proto(0, 1, True)
    assert len(transactions) == 1
    assert len(events_for_versions.events_for_version) == 1
    assert len(events_for_versions.events_for_version[0].events) == 0

def test_get_tx_latest():
    c = libra.Client("testnet")
    ver = c.get_latest_transaction_version()
    transactions, events_for_versions = c.get_transactions_proto(ver-2, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2

def test_get_tx_zero():
    c = libra.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(1, 0, True)
    assert len(transactions) == 0

def test_get_tx_invalid():
    c = libra.Client("testnet")
    with pytest.raises(ValueError):
        c.get_transactions_proto(1, -1, True)

def test_get_latest_transaction_version():
    c = libra.Client("testnet")
    ver = c.get_latest_transaction_version()
    assert ver > 0

def test_get_balance():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    balance = c.get_balance(address)
    assert balance > 0

def test_get_account_resource():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    ret = c.get_account_resource(address)
    assert len(ret.authentication_key) == 32
    assert ret.balance > 0
    assert ret.delegated_key_rotation_capability == False
    assert ret.delegated_withdrawal_capability == False
    assert ret.received_events.count > 0
    assert len(ret.received_events.key) == 32
    assert ret.sent_events.count > 0
    assert len(ret.sent_events.key) == 32
    assert ret.sequence_number > 0
    addr = b'\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\nU\x0c\x18'
    assert addr == bytes.fromhex(address)
    ret2 = c.get_account_resource(addr)
    assert ret.delegated_withdrawal_capability == ret2.delegated_withdrawal_capability
    assert ret2.received_events.count >= ret.received_events.count
    assert ret2.sent_events.count >= ret.sent_events.count
    assert ret2.sequence_number >= ret.sequence_number


def test_account_not_exsits():
    address = "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e21"
    c = libra.Client("testnet")
    with pytest.raises(libra.client.AccountError):
        balance = c.get_account_state(address)

def test_get_account_transaction_proto():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    txn, usecs = c.get_account_transaction_proto(address, 1, True)
    len(str(usecs)) == 16
    assert usecs//1000_000 > 1570_000_000
    assert txn.events.events[0].sequence_number == 1
    assert len(txn.signed_transaction.signed_txn) > 0
    assert txn.version > 0
    assert txn.proof.HasField("ledger_info_to_transaction_info_proof")
    assert txn.proof.HasField("transaction_info")


def test_transfer_coin():
    wallet = libra.WalletLibrary.new()
    a0 = wallet.new_account()
    a1 = wallet.new_account()
    c = libra.Client("testnet")
    c.mint_coins_with_faucet_service(a0.address.hex(), 1234, True)
    balance0 = c.get_balance(a0.address)
    try:
        balance1 = c.get_balance(a1.address)
    except libra.client.AccountError:
        balance1 = 0
    ret = c.transfer_coin(a0, a1.address, 1234, unit_price=0, is_blocking=True)
    assert bytes(ret.raw_txn.sender) == a0.address
    assert ret.raw_txn.sequence_number == 0
    assert c.get_balance(a0.address) == balance0 - 1234
    assert c.get_balance(a1.address) == balance1 + 1234

def test_client_init():
    c = libra.Client.new("localhost","8080", "libra/consensus_peers.config.toml")
    assert c.host == "localhost"
    assert c.port == 8080
    assert hasattr(c, "faucet_host") == False
    assert c.verbose == True
    assert c.faucet_account is not None
    assert len(c.validator_verifier.validators) > 0
    address, key = c.validator_verifier.validators.popitem()
    assert len(address) == libra.account_address.ADDRESS_LENGTH
    assert len(key._key) == 32
    c2 = libra.Client("testnet")
    assert c2.host == "ac.testnet.libra.org"
    assert c2.port == 8000
    assert c2.faucet_host == "faucet.testnet.libra.org"
    assert c2.verbose == True
    assert c2.faucet_account is None
    assert len(c2.validator_verifier.validators) > 0
    with pytest.raises(libra.LibraNetError):
        libra.Client("xnet")
    with pytest.raises(libra.LibraNetError):
        libra.Client("mainnet")
    with pytest.raises(TypeError):
        libra.Client.new("localhost", 8000)
    with pytest.raises(FileNotFoundError):
        libra.Client.new("localhost", 8000, "non_exsits_file")