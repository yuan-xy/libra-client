import libra
from libra.transaction import *
from libra.contract_event import ContractEvent
import os
import pytest
#import pdb


def test_get_transaction():
    c = libra.Client("testnet")
    stx = c.get_transaction(1, True)
    print(stx)
    assert isinstance(stx, libra.block_metadata.BlockMetadata) == True
    assert stx.previous_block_votes == {}
    assert len(stx.proposer) == 32
    assert len(stx.id) == 32
    assert stx.timestamp_usec > 1570_000_000_000_000
    assert len(stx.events) == 0
    info = stx.transaction_info
    assert info.major_status == 4001
    assert info.gas_used == 0

def test_get_transactions3():
    c = libra.Client("testnet")
    txs = c.get_transactions(0, limit=3, fetch_events=True)
    assert len(txs) == 3



def test_get_transaction_without_events():
    c = libra.Client("testnet")
    assert hasattr(c, "latest_time") == False
    transactions = c.get_transactions(1, 1, False)
    assert len(transactions) == 1
    assert hasattr(transactions[0], 'success') == False
    assert hasattr(c, "latest_time") == True
    assert c.latest_time > 1570_000_000_000_000


def test_get_tx_with_events():
    c = libra.Client("testnet")
    transactions, events_for_versions = c.get_transactions_proto(1, 2, True)
    if c.client_known_version == 1:
        return
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
    events = events_for_versions.events_for_version[0].events
    assert len(events) == 4
    ces = [ContractEvent.from_proto(x) for x in events]
    assert len(ces) == 4


def test_get_tx_latest():
    c = libra.Client("testnet")
    ver = c.get_latest_transaction_version()
    if ver == 1:
        return
    transactions, events_for_versions = c.get_transactions_proto(ver-2, 2, True)
    assert len(transactions) == 2
    assert len(events_for_versions.events_for_version) == 2

def test_get_tx_zero():
    c = libra.Client("testnet")
    with pytest.raises(ValueError):
        c.get_transactions_proto(1, 0, True)


def test_get_tx_invalid():
    c = libra.Client("testnet")
    with pytest.raises(TypeError):
        c.get_transactions_proto(1, -1, True)

def test_get_latest_transaction_version():
    c = libra.Client("testnet")
    ver = c.get_latest_transaction_version()
    assert ver > 0

def test_get_balance():
    address = libra.AccountConfig.transaction_fee_address()
    c = libra.Client("testnet")
    balance = c.get_balance(address)
    assert balance >= 0

def test_get_account_resource():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    ret = c.get_account_resource(address)
    assert len(ret.authentication_key) == 32
    assert ret.balance > 0
    assert ret.delegated_key_rotation_capability == False
    assert ret.delegated_withdrawal_capability == False
    assert ret.received_events.count > 0
    assert len(ret.received_events.key) == libra.event.EVENT_KEY_LENGTH
    assert ret.sent_events.count > 0
    assert len(ret.sent_events.key) == libra.event.EVENT_KEY_LENGTH
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
    if txn.version == 0:
        return
    assert txn.proof.HasField("ledger_info_to_transaction_info_proof")
    assert txn.proof.HasField("transaction_info")
    assert len(txn.transaction.transaction) > 0
    if txn.proof.transaction_info.major_status == 4001:
        assert txn.events.events[0].sequence_number == 1


def test_transfer_coin():
    wallet = libra.WalletLibrary.new()
    a0 = wallet.new_account()
    a1 = wallet.new_account()
    c = libra.Client("testnet")
    c.mint_coins(a0.address.hex(), 1234, True)
    balance0 = c.get_balance(a0.address, retry=True)
    balance1 = c.get_balance(a1.address, retry=True)
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

def test_client_testnet():
    c2 = libra.Client("testnet")
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
    assert len(c2.validator_verifier.validators) > 0

def test_client_error():
    with pytest.raises(libra.LibraNetError):
        libra.Client("xnet")
    with pytest.raises(libra.LibraNetError):
        libra.Client("mainnet")
    with pytest.raises(TypeError):
        libra.Client.new("localhost", 8000)
    with pytest.raises(FileNotFoundError):
        libra.Client.new("localhost", 8000, "non_exsits_file")

def test_timeout():
    c = libra.Client("testnet")
    c.timeout = 0.001
    with pytest.raises(Exception) as excinfo:
        stx = c.get_transaction(1, True)
    error = excinfo.value
    assert error.code().name == 'DEADLINE_EXCEEDED'
    assert error.details() == 'Deadline Exceeded'
