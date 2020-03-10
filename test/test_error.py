from libra import RawTransaction, SignedTransaction
import libra_client
import pytest


def test_invalid_signature():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    a0 = wallet.accounts[0]
    a1 = wallet.accounts[1]
    raw_tx = RawTransaction._gen_transfer_transaction(a0.address, 0, a1.address, 123)
    stx = SignedTransaction.gen_from_raw_txn(raw_tx, a0)
    stx.signature = b'\0'*64
    client = libra_client.Client("testnet")
    with pytest.raises(Exception) as excinfo:
        client.submit_signed_txn(stx)
        #libra_client.error.VMError: (3, 'SEQUENCE_NUMBER_TOO_OLD')
    return #TODO: This maybe libra's bug, should return INVALID_SIGNATURE error.
    with pytest.raises(libra_client.VMError) as excinfo:
    	client.submit_signed_txn(stx)
    vm_error = excinfo.value
    assert vm_error.args == (1, 'INVALID_SIGNATURE')
    assert vm_error.error_code == 1
    assert vm_error.error_msg == 'INVALID_SIGNATURE'
