import libra
from tempfile import NamedTemporaryFile
from libra.key_factory import has_sha3
import pytest
import pdb


def test_wallet():
    if not has_sha3():
        return
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    a0 = wallet.accounts[0]
    assert a0.address_hex == "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e2f"
    assert a0.public_key_hex == "d1f4e85a3582015deb92d8aba35061a8032865d754a364d2429d475d10829c2a"
    assert a0.private_key_hex == "177bb836b2bb9be29f5accdf74a95d917946001282d7ee74b18d0c81764ee383"
    a1 = wallet.accounts[1]
    assert a1.address_hex == "f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde"
    assert a1.public_key_hex == "6b72f3922ccbe671409c5ad0552f93888427f466ea0b7fdf3f066b31bce5c6a6"
    assert a1.private_key_hex == "2aa7e79ffe6bcb110b2a736ef4d37ad471c88b6f5be833cf1f2989ef12db05be"
    tmp = NamedTemporaryFile('w+t')
    wallet.write_recovery(tmp.name)
    with open('test/test.wallet') as f0:
            data0 = f0.read()
            with open(tmp.name) as f1:
                data1 = f1.read()
                arr0 = data0.split(";")
                arr1 = data1.split(";")
                assert arr0[0] == arr1[0]
                assert int(arr0[1]) == int(arr1[1])
    tmp.close()

def test_new_wallet():
    wallet = libra.WalletLibrary.new()
    assert wallet.child_count == 0
    assert len(wallet.mnemonic.split()) == 18

def test_get_account_by_address_or_refid():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    accounts = wallet.accounts
    assert accounts[0] == wallet.get_account_by_address_or_refid("0")
    assert accounts[1] == wallet.get_account_by_address_or_refid("1")
    with pytest.raises(ValueError):
        wallet.get_account_by_address_or_refid("2")
    assert accounts[0] == wallet.get_account_by_address_or_refid("7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e2f")
    with pytest.raises(ValueError):
        wallet.get_account_by_address_or_refid("0"*64)
    with pytest.raises(ValueError):
        wallet.get_account_by_address_or_refid("0"*63)


def test_rotate_file():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    wallet.rotate_key(1, 0)
    tmp = NamedTemporaryFile('w+t')
    wallet.write_recovery(tmp.name)
    wallet2 = libra.WalletLibrary.recover(tmp.name)
    assert wallet2.child_count == 2
    wallet2.accounts[0] == wallet.accounts[0]
    wallet2.accounts[1].address == wallet.accounts[1].address
    wallet2.accounts[1].public_key == wallet.accounts[0].public_key

def test_rotate_file2():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert wallet.child_count == 2
    wallet.rotate_key("1", "0")
    tmp = NamedTemporaryFile('w+t')
    wallet.write_recovery(tmp.name)
    wallet2 = libra.WalletLibrary.recover(tmp.name)
    assert wallet2.child_count == 2
    wallet2.accounts[0] == wallet.accounts[0]
    wallet2.accounts[1].address == wallet.accounts[1].address
    wallet2.accounts[1].public_key == wallet.accounts[0].public_key






