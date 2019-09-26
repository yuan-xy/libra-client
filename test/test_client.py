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
    txn = c.get_transaction(1)
    assert len(txn.signed_txn) > 0
    stx = SignedTransaction.deserialize(txn.signed_txn)
    assert bytes(stx.raw_txn.sender).hex() == libra.AccountConfig.association_address()
    assert stx.raw_txn.sequence_number == 1
    assert stx.raw_txn.payload.index == 2
    assert stx.raw_txn.payload.Script == True
    assert stx.raw_txn.payload.value.code == RawTransaction.get_script_bytecode("mint")
    assert stx.raw_txn.payload.value.args[0].index == 1
    assert stx.raw_txn.payload.value.args[0].Address == True
    assert stx.raw_txn.payload.value.args[1].index == 0
    assert stx.raw_txn.payload.value.args[1].U64 == True
    assert stx.raw_txn.payload.value.args[1].value == 100000000
    assert stx.raw_txn.max_gas_amount == 140000
    assert stx.raw_txn.gas_unit_price == 0
    assert stx.raw_txn.expiration_time > 1_568_000_000
    assert stx.raw_txn.expiration_time < 11_568_000_000
    assert len(stx.public_key) == 32
    assert len(stx.signature) == 64
    raw_txn_bytes = stx.raw_txn.serialize()
    raw_txn_hash = libra.Client.raw_tx_hash(raw_txn_bytes)
    libra.Client.verify_transaction(raw_txn_hash, stx.public_key, stx.signature)


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
    txn = c.get_account_transaction(address, 1, True)
    assert txn.events.events[0].sequence_number == 1
    assert len(txn.signed_transaction.signed_txn) > 0
    assert txn.version > 0
    assert txn.proof.HasField("ledger_info_to_transaction_info_proof")
    assert txn.proof.HasField("transaction_info")



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
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra.Client("testnet")
    c.mint_coins_with_faucet_service(a0.address.hex(), 1234, True)
    balance0 = c.get_balance(a0.address)
    try:
        balance1 = c.get_balance(a1.address)
    except libra.client.AccountError:
        balance1 = 0
    ret = c.transfer_coin(a0, a1.address, 1234, is_blocking=True)
    assert ret.ac_status.code == libra.proto.admission_control_pb2.AdmissionControlStatusCode.Accepted
    assert c.get_balance(a0.address) == balance0 - 1234
    assert c.get_balance(a1.address) == balance1 + 1234

def test_client_init():
    c = libra.Client.new("localhost","8080", "libra/consensus_peers.config.toml")
    assert c.host == "localhost"
    assert c.port == 8080
    assert hasattr(c, "faucet_host") == False
    assert len(c.validators) > 0
    address, key = c.validators.popitem()
    assert len(address) == 64
    assert len(key._key) == 32
    c2 = libra.Client("testnet")
    assert c2.host == "ac.testnet.libra.org"
    assert c2.port == 8000
    assert c2.faucet_host == "faucet.testnet.libra.org"
    assert len(c2.validators) > 0
    with pytest.raises(libra.LibraNetError):
        libra.Client("xnet")
    with pytest.raises(libra.LibraNetError):
        libra.Client("mainnet")
    with pytest.raises(TypeError):
        libra.Client.new("localhost", 8000)
    with pytest.raises(FileNotFoundError):
        libra.Client.new("localhost", 8000, "non_exsits_file")