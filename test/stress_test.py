import libra
from libra.transaction import *
import os, time
import pytest
import pdb

def is_in_ci():
    if 'TRAVIS' in os.environ:
        return True
    if 'CI' in os.environ and os.environ['CI'] == 'true':
        return True
    return False


def test_429():
    if is_in_ci():
        return
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    c = libra.Client("testnet")
    try:
        while True:
            time.sleep(1)
            a1 = wallet.new_account()
            c.transfer_coin(a0, a1.address, 1, unit_price=0, is_blocking=False)
    except Exception as err:
        assert err.details() == 'Received http2 header with status: 429'
        assert err.__class__.__name__ == '_Rendezvous'
        print(err)


def test_seq_too_old():
    if is_in_ci():
        return
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    c = libra.Client("testnet")
    try:
        while True:
            a1 = wallet.new_account()
            c.transfer_coin(a0, a1.address, 1, unit_price=0, is_blocking=False)
    except Exception as err:
        assert err.error_code == 3
        assert err.error_msg == 'SEQUENCE_NUMBER_TOO_OLD'
        print(err)

