import libra
from libra.transaction import *
import struct
import pdb


def test_transaction():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction.gen_transfer_transaction(a0.address, 0, a1.address, 123)
    assert raw_tx.max_gas_amount == 140000
    assert raw_tx.gas_unit_price == 0
    # assert raw_tx.sender_account == a0.address
    # assert len(raw_tx.program.arguments) == 2


def test_address():
    hex_a = "000000000000000000000000000000000000000000000000000000000a550c18"
    int_a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 85, 12, 24]
    bytes_a = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\nU\x0c\x18'
    assert hex_a.encode() == b"000000000000000000000000000000000000000000000000000000000a550c18"
    assert bytes.fromhex(hex_a) == bytes_a
    assert bytes(int_a) == bytes_a
    assert int_list_to_hex(int_a) == hex_a
    assert bytes_a.hex() == hex_a
    assert bytes_to_int_list(bytes_a) == int_a
    assert hex_to_int_list(hex_a) == int_a