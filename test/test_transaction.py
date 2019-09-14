import libra
from mnemonic import Mnemonic
from nacl.signing import SigningKey

import pdb

def test_transaction():
    kfac = libra.KeyFactory.read_wallet_file('test/test.wallet')
    child0 = kfac.private_child(0)
    a0 = libra.Account(child0)
    child1 = kfac.private_child(1)
    a1 = libra.Account(child1)
    t = libra.Transaction.gen_transfer_transaction(a1, 123)
    sequence_number = 0
    raw_tx = t.to_raw_tx_proto(a0, sequence_number)
    assert raw_tx.max_gas_amount == 140000
    assert raw_tx.gas_unit_price == 0
    assert raw_tx.sender_account == a0.address
    assert len(raw_tx.program.arguments) == 2
