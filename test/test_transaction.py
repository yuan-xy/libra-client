import libra


def test_transaction():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    t = libra.Transaction.gen_transfer_transaction(a1, 123)
    sequence_number = 0
    raw_tx = t.to_raw_tx_proto(a0, sequence_number)
    assert raw_tx.max_gas_amount == 140000
    assert raw_tx.gas_unit_price == 0
    assert raw_tx.sender_account == a0.address
    assert len(raw_tx.program.arguments) == 2
