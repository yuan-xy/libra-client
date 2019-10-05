import libra
from libra.transaction import *
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
