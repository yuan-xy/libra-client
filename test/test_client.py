import libra
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

def test_account_not_exsits():
    address = "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e21"
    c = libra.Client("testnet")
    with pytest.raises(libra.client.AccountError):
        balance = c.get_balance(address)

def test_get_account_transaction():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    #pdb.set_trace()
    txn = c.get_account_transaction(address, 6600, True)
    assert len(txn.signed_transaction.raw_txn_bytes) > 0

def test_mint():
    address = "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e20"
    c = libra.Client("testnet")
    try:
        balance = c.get_balance(address)
    except libra.client.AccountError:
        balance = 0
    c.mint_coins_with_faucet_service(address, 12345, True)
    balance2 = c.get_balance(address)
    assert (balance2 - balance) % 12345 == 0 # tolerate parallel mint

def test_transfer_coin():
    kfac = libra.KeyFactory.read_wallet_file('test/test.wallet')
    child0 = kfac.private_child(0)
    a0 = libra.Account(child0)
    child1 = kfac.private_child(1)
    a1 = libra.Account(child1)
    c = libra.Client("testnet")
    balance0 = c.get_balance(a0.address)
    balance1 = c.get_balance(a1.address)
    ret = c.transfer_coin(a0, a1, 1234, True)
    assert ret.ac_status.code == libra.proto.admission_control_pb2.AdmissionControlStatusCode.Accepted
    assert c.get_balance(a0.address) == balance0 - 1234
    assert c.get_balance(a1.address) == balance1 + 1234

