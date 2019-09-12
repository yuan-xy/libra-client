import libra
import pdb

def test_events():
    address = libra.AccountConfig.association_address()
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
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    balance = c.get_balance(address)
    assert balance > 0

def test_get_account_transaction():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    #pdb.set_trace()
    txn = c.get_account_transaction(address, 6600, True)
    assert len(txn.signed_transaction.raw_txn_bytes) > 0

def test_mint():
    address = "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e2f"
    c = libra.Client("testnet")
    balance = c.get_balance(address)
    c.mint_coins_with_faucet_service(address, 12345, True)
    balance2 = c.get_balance(address)
    assert balance + 12345 == balance2


