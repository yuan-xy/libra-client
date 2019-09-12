import libra
import pdb

def test_events():
    address = "000000000000000000000000000000000000000000000000000000000a550c18"
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    #pdb.set_trace()
    assert len(events) == 2

def test_get_transaction():
    c = libra.Client("testnet")
    txn = c.get_transaction(1)
    assert len(txn.raw_txn_bytes) > 0

def test_get_latest_transaction_version():
    c = libra.Client("testnet")
    ver = c.get_latest_transaction_version()
    assert ver > 0

def test_get_balance():
    address = "000000000000000000000000000000000000000000000000000000000a550c18"
    c = libra.Client("testnet")
    balance = c.get_balance(address)
    assert balance > 0

def test_get_account_transaction():
    address = "000000000000000000000000000000000000000000000000000000000a550c18"
    c = libra.Client("testnet")
    #pdb.set_trace()
    txn = c.get_account_transaction(address, 6600, True)
    assert len(txn.raw_txn_bytes) > 0
