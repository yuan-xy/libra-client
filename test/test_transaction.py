import libra
from libra.transaction import *
from libra.client import TransactionError, TransactionTimeoutError
import pytest
import nacl
import pdb


def test_raw_txn():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction.gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == 140000
    assert raw_tx.gas_unit_price == 0
    assert bytes(raw_tx.sender) == a0.address
    assert raw_tx.payload.enum_name == "Script"
    assert raw_tx.payload.index == 2
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == RawTransaction.get_script_bytecode("peer_to_peer_transfer")
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
    raw_tx = RawTransaction.gen_transfer_transaction(a0.address, 0, a1.address, 123)
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
    if diff > 0:
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
    c.transfer_coin(a0, a1.address, balance0+1, is_blocking=False)
    assert False == c.wait_for_transaction(a0.address, sequence_number) #no events emitted

