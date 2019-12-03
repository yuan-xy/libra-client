import libra
from libra.transaction import *
from libra.client import TransactionError, TransactionTimeoutError
from canoser import Uint64
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
import pytest
import nacl
#import pdb


def test_raw_txn():
    assert RawTransaction.__doc__.startswith("RawTransaction is the portion of a transaction that a client signs")
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == 140000
    assert raw_tx.gas_unit_price == 0
    assert bytes(raw_tx.sender) == a0.address
    assert raw_tx.payload.enum_name == "Script"
    assert raw_tx.payload.index == 2
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_transfer")
    assert script.args[0].index == 1
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[1].index == 0
    assert script.args[1].U64 == True
    assert script.args[1].value == 123

def test_signed_txn():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    stx.check_signature()
    with pytest.raises(nacl.exceptions.BadSignatureError):
        stx.signature = [0]*64
        stx.check_signature()

def test_wait_for_transaction_timeout():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra.Client("testnet")
    diff = c._get_time_diff()
    if diff < 0:
        with pytest.raises(TransactionTimeoutError):
            c.transfer_coin(a0, a1.address, 1, unit_price=0, is_blocking=True, txn_expiration=0)

def test_gax_too_large():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra.Client("testnet")
    balance0 = c.get_balance(a0.address)
    with pytest.raises(TransactionError):
        c.transfer_coin(a0, a1.address, 1, unit_price=balance0)
    with pytest.raises(TransactionError):
        c.transfer_coin(a0, a1.address, 1, max_gas=1_000_001)
    with pytest.raises(TransactionError):
        c.transfer_coin(a0, a1.address, 1, max_gas=balance0+1, unit_price=10000)


def test_amount_zero():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra.Client("testnet")
    ret = c.transfer_coin(a0, a1.address, 0, is_blocking=True)
    proto, _ = c.get_account_transaction_proto(ret.raw_txn.sender, ret.raw_txn.sequence_number, True)
    stx = Transaction.deserialize(proto.transaction.transaction).value
    assert proto.version > 1
    assert len(proto.events.events) == 0
    assert stx == ret
    assert proto.proof.transaction_info.major_status == 4016


def test_amount_illegal():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra.Client("testnet")
    sequence_number = c.get_sequence_number(a0.address)
    balance0 = c.get_balance(a0.address)
    with pytest.raises(Exception):
        c.transfer_coin(a0, a1.address, -1)
    with pytest.raises(Exception):
        c.transfer_coin(a0, a1.address, 0.1)
    try:
        c.transfer_coin(a0, a1.address, balance0+99999999, is_blocking=False)
        assert False == c.wait_for_transaction(a0.address, sequence_number) #no events emitted
    except libra.client.TransactionError as err:
        #TODO: check this err. sometimes will throw this err.
        #code: InvalidUpdate
        #message: "Failed to update gas price to 0"
        pass

def test_query():
    c = libra.Client("testnet")
    txs = c.get_transactions(1, "1")
    txs = c.get_transactions("1", 1)
    txs = c.get_transactions(1, "1", False)
    with pytest.raises(TypeError):
        c.get_transactions(1, True)


def test_get_transaction_invalid():
    client = libra.Client("testnet")
    with pytest.raises(TypeError):
        client.get_transaction(-1)
    tx = client.get_transaction(Uint64.max_value)
    assert tx is None
    with pytest.raises(TypeError):
        client.get_transaction(Uint64.max_value+1)

def test_tx_id_overflow():
    client = libra.Client("testnet")
    start_version = Uint64.max_value+1
    request = UpdateToLatestLedgerRequest()
    item = request.requested_items.add()
    with pytest.raises(ValueError):
        item.get_transactions_request.start_version = start_version
    with pytest.raises(ValueError):
        item.get_transactions_request.start_version = -1
    # item.get_transactions_request.limit = 1
    # item.get_transactions_request.fetch_events = False
    # resp = client.update_to_latest_ledger(request)
    # print(resp)