import libra
import libra_client
from libra import Address
from libra.transaction import *
from libra.contract_event import ContractEvent
from canoser import Uint64
import os
import pytest
import requests

#import pdb


def test_get_transaction():
    c = libra_client.Client("testnet")
    stx = c.get_transaction(1, True)
    print(stx)
    assert isinstance(stx, libra.block_metadata.BlockMetadata) == True
    assert stx.previous_block_votes == []
    assert len(stx.proposer) == Address.LENGTH
    assert len(stx.id) == 32
    assert stx.timestamp_usecs == 0 or stx.timestamp_usecs > 1570_000_000_000_000
    assert len(stx.events) == 1
    be = libra.block_metadata.NewBlockEvent.deserialize(stx.events[0].event_data)
    assert be.round == stx.round
    info = stx.transaction_info
    assert info.major_status == 4001
    assert info.gas_used == 0

def test_get_transactions3():
    c = libra_client.Client("testnet")
    txs = c.get_transactions(0, limit=3, fetch_events=True)
    assert len(txs) == 3



def test_get_transaction_without_events():
    c = libra_client.Client("testnet")
    assert hasattr(c, "latest_time") == False
    transactions = c.get_transactions(1, 1, False)
    assert len(transactions) == 1
    assert hasattr(transactions[0], 'success') == False
    assert hasattr(c, "latest_time") == True
    assert c.latest_time > 1570_000_000_000_000


def test_get_tx_with_events():
    c = libra_client.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(1, 2, True)
    if c.state.version == 1:
        return
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2

def test_get_tx_from_zero():
    c = libra_client.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(0, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2
    assert c.state.version > 0
    assert c.state.verifier.value.epoch > 0
    assert len(c.state.verifier.value.verifier.address_to_validator_info) > 0
    assert c.state.latest_epoch_change_li is not None
    info = c.state.latest_epoch_change_li.ledger_info
    assert info.timestamp_usecs == info.commit_info.timestamp_usecs
    assert info.consensus_block_id == info.commit_info.id
    assert info.transaction_accumulator_hash == info.commit_info.executed_state_id
    assert info.next_validator_set == info.commit_info.next_validator_set
    transactions, events_for_versions = c.get_transactions_proto(0, 1, True)
    assert len(transactions) == 1
    assert len(events_for_versions.events_for_version) == 1
    events = events_for_versions.events_for_version[0].events
    assert len(events) == 4
    ces = [ContractEvent.from_proto(x) for x in events]
    assert len(ces) == 4


def test_get_tx_latest():
    c = libra_client.Client("testnet")
    ver = c.get_latest_transaction_version()
    if ver == 1:
        return
    transactions, events_for_versions = c.get_transactions_proto(ver-2, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2

def test_get_tx_zero():
    c = libra_client.Client("testnet")
    with pytest.raises(ValueError):
        c.get_transactions_proto(1, 0, True)


def test_get_tx_invalid():
    c = libra_client.Client("testnet")
    with pytest.raises(TypeError):
        c.get_transactions_proto(1, -1, True)

def test_get_latest_transaction_version():
    c = libra_client.Client("testnet")
    ver = c.get_latest_transaction_version()
    assert ver > 0

def test_get_balance():
    address = libra.AccountConfig.transaction_fee_address()
    c = libra_client.Client("testnet")
    balance = c.get_balance(address)
    assert balance >= 0

def test_get_account_resource():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    ret = c.get_account_resource(address)
    assert len(ret.authentication_key) == 32
    assert ret.delegated_key_rotation_capability == False
    assert ret.delegated_withdrawal_capability == False
    assert ret.received_events.count > 0
    assert len(ret.received_events.key) == libra.event.EVENT_KEY_LENGTH
    assert ret.sent_events.count > 0
    assert len(ret.sent_events.key) == libra.event.EVENT_KEY_LENGTH
    assert ret.sequence_number > 0
    balance = c.get_balance(address)
    assert balance > 0
    addr = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nU\x0c\x18'
    assert addr == bytes.fromhex(address)
    ret2 = c.get_account_resource(addr)
    assert ret.delegated_withdrawal_capability == ret2.delegated_withdrawal_capability
    assert ret2.received_events.count >= ret.received_events.count
    assert ret2.sent_events.count >= ret.sent_events.count
    assert ret2.sequence_number >= ret.sequence_number


def test_account_not_exsits():
    address = "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e21"[32:]
    c = libra_client.Client("testnet")
    with pytest.raises(libra_client.client.AccountError):
        balance = c.get_account_state(address)

def test_get_acc_txns_with_client_known_version():
    address = libra.AccountConfig.association_address()
    client = libra_client.Client("testnet")
    client.state.version = 2
    with pytest.raises(libra.validator_verifier.VerifyError):
        #need validator proof
        client.get_account_transaction_proto(address, 1, False)
    client.state.version = 0
    client.get_account_transaction_proto(address, 1, False)
    assert client.state.version > 0
    client.get_account_transaction_proto(address, 1, False)



def test_get_account_transaction_proto():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    txn, usecs = c.get_account_transaction_proto(address, 1, True)
    len(str(usecs)) == 16
    assert usecs//1000_000 > 1570_000_000
    if txn.version == 0:
        return
    assert txn.proof.HasField("ledger_info_to_transaction_info_proof")
    assert txn.proof.HasField("transaction_info")
    assert len(txn.transaction.transaction) > 0
    if txn.proof.transaction_info.major_status == 4001:
        assert txn.events.events[0].sequence_number == 1

def test_get_account_transaction_non_exists():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    txn, usecs = c.get_account_transaction_proto(address, Uint64.max_value, True)
    assert txn.__str__() == ''


def test_transfer_coin():
    wallet = libra_client.WalletLibrary.new()
    a0 = wallet.new_account()
    a1 = wallet.new_account()
    c = libra_client.Client("testnet")
    c.mint_coins(a0.address, a0.auth_key_prefix, 1234_000, True)
    balance0 = c.get_balance(a0.address, retry=True)
    balance1 = c.get_balance(a1.address, retry=True)
    ret = c.create_account(a0, a1.address, a1.auth_key_prefix, is_blocking=True)
    assert ret.raw_txn.sequence_number == 0
    ret = c.transfer_coin(a0, a1.address, 123, unit_price=1, is_blocking=True)
    assert bytes(ret.raw_txn.sender) == a0.address
    assert ret.raw_txn.sequence_number == 1
    assert c.get_balance(a0.address) <= balance0 - 123
    assert c.get_balance(a1.address) == balance1 + 123

def test_client_init():
    client = libra_client.Client.new("localhost","8080")
    assert client.host == "localhost"
    assert client.port == 8080
    assert hasattr(client, "faucet_host") == False
    assert client.verbose == True
    assert client.faucet_account is not None
    assert client.state.version == 0
    assert client.state.verifier.enum_name == 'TrustedVerifier'
    assert client.state.verifier.value.epoch == 0
    assert client.state.verifier.value.verifier.address_to_validator_info == {}
    assert client.state.latest_epoch_change_li is None


def test_client_testnet():
    c2 = libra_client.Client("testnet")
    try:
        tests = os.environ['TESTNET_LOCAL'].split(";")
        assert c2.host == tests[0]
        assert c2.port == int(tests[1])
        return
    except KeyError:
        pass
    assert c2.host == "ac.testnet.libra.org"
    assert c2.port == 8000
    assert c2.faucet_host == "faucet.testnet.libra.org"
    assert c2.verbose == True
    assert c2.faucet_account is None
    c2.init_trusted_state(None)


def test_client_error():
    with pytest.raises(libra_client.client.LibraNetError):
        libra_client.Client("xnet")
    with pytest.raises(libra_client.client.LibraNetError):
        libra_client.Client("mainnet")
    with pytest.raises(FileNotFoundError):
        libra_client.Client.new("localhost", 8000, "non_exsits_file")

def test_timeout():
    c = libra_client.Client("testnet")
    c.timeout = 0.001
    with pytest.raises(Exception) as excinfo:
        stx = c.get_transaction(1, True)
    error = excinfo.value
    assert error.code().name == 'DEADLINE_EXCEEDED'
    assert error.details() == 'Deadline Exceeded'
