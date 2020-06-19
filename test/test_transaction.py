import libra_client
from libra.crypto.ed25519 import ED25519_PRIVATE_KEY_LENGTH, ED25519_SIGNATURE_LENGTH
from libra.transaction import *
from libra_client.error import LibraError, AccountError, TransactionError, TransactionTimeoutError
from canoser import Uint64
import pytest
import nacl
import os


def test_raw_txn():
    assert RawTransaction.__doc__.startswith("RawTransaction is the portion of a transaction that a client signs")
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == MAX_GAS_AMOUNT
    assert raw_tx.gas_unit_price == 0
    assert bytes(raw_tx.sender) == a0.address
    assert raw_tx.payload.enum_name == "Script"
    assert raw_tx.payload.index == 1
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert script.args[0].index == 3
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[1].index == 1
    assert script.args[1].U64 == True
    assert script.args[1].value == 123


def test_raw_txn_with_metadata():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 9, metadata=bytes([2,3,4]))
    assert raw_tx.payload.value_type == Script
    script = raw_tx.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert script.args[0].index == 3
    assert script.args[0].Address == True
    assert script.args[0].enum_name == 'Address'
    assert script.args[1].index == 1
    assert script.args[1].U64 == True
    assert script.args[1].value == 9
    assert script.args[2].index == 4
    assert script.args[2].U8Vector == True
    assert script.args[2].value == bytes([2,3,4])


def test_signed_txn():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    stx.check_signature()
    with pytest.raises(nacl.exceptions.BadSignatureError):
        authenticator = TransactionAuthenticator.ed25519(a0.public_key, b'\0'*ED25519_SIGNATURE_LENGTH)
        stx.authenticator = authenticator
        stx.check_signature()


def test_gax_too_large():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra_client.Client("testnet")
    try:
        balance0 = c.get_balance(a0.address)
    except AccountError:
        balance0 = 0
    with pytest.raises(LibraError):
        c.transfer_coin(a0, a1.address, 1, gas_unit_price=balance0)
    with pytest.raises(LibraError):
        c.transfer_coin(a0, a1.address, 1, max_gas_amount=1_000_000_001)
    with pytest.raises(LibraError):
        c.transfer_coin(a0, a1.address, 1, max_gas_amount=balance0+1, gas_unit_price=10000)


def test_amount_zero():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra_client.Client("testnet")
    try:
        ret = c.transfer_coin(a0, a1.address, 0, is_blocking=True)
    except LibraError as ae:
        pass



def test_transfer_to_self():
    return
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    c = libra_client.Client("testnet")
    balance = c.get_balance(a0.address)
    if balance == 0:
        c.mint_coins(a0.address, 1000000, is_blocking=True)
    ret = c.transfer_coin(a0, a0.address, 1, is_blocking=True)
    stx = c.get_account_transaction(ret.raw_txn.sender, ret.raw_txn.sequence_number, True)
    assert proto.version > 1
    assert len(proto.events.events) == 2
    assert proto.proof.transaction_info.major_status == 4001
    assert balance == c.get_balance(a0.address)



def test_amount_illegal():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    c = libra_client.Client("testnet")
    sequence_number = c.get_sequence_number(a0.address)
    balance0 = c.get_balance(a0.address)
    with pytest.raises(Exception):
        c.transfer_coin(a0, a1.address, -1)
    with pytest.raises(Exception):
        c.transfer_coin(a0, a1.address, 0.1)
    try:
        c.transfer_coin(a0, a1.address, balance0+99999999, is_blocking=False)
        c.wait_for_transaction(a0.address, sequence_number) #no events emitted
    except LibraError as mpe:
        pass


def test_query():
    c = libra_client.Client("testnet")
    with pytest.raises(LibraError):
        txs = c.get_transactions(1, "1")
    with pytest.raises(LibraError):
        txs = c.get_transactions("1", 1)
    with pytest.raises(LibraError):
        txs = c.get_transactions(1, "1", False)
    with pytest.raises(LibraError):
        c.get_transactions(1, True)


def test_get_transaction_invalid():
    client = libra_client.Client("testnet")
    with pytest.raises(LibraError):
        client.get_transaction(-1)
    tx = client.get_transaction(Uint64.max_value)
    assert tx is None
    with pytest.raises(LibraError):
        client.get_transaction(Uint64.max_value+1)


def test_transfer_with_metadata():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    client = libra_client.Client("testnet")
    balance = client.get_balance(a0.address)
    if balance == 0:
        client.mint_coins(a0.address, a0.auth_key_prefix, 1000000, is_blocking=True)

    try:
        client.create_account(a0, a1.address, a1.auth_key_prefix, is_blocking=True)
    except libra_client.error.VMError as err:
        if err.error_code == 4016:
            pass
        else:
            raise
    except Exception:
        if not 'TESTNET_LOCAL' in os.environ:
            return
        else:
            raise

    ret = client.transfer_coin(a0, a1.address, 1, metadata=bytes([3,4,5]), is_blocking=True)
    script = ret.raw_txn.payload.value
    assert script.code == Script.get_script_bytecode("peer_to_peer_with_metadata")
    assert bytes(script.args[0].value) == a1.address
    assert script.args[1].value == 1
    assert script.args[2].value == bytes([3,4,5])
    tx = client.get_account_transaction(ret.raw_txn.sender, ret.raw_txn.sequence_number, True)
    assert tx.version > 1


