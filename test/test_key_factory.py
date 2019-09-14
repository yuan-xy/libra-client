import libra
from mnemonic import Mnemonic
from nacl.signing import SigningKey

import pdb

def test_key():
    m = Mnemonic("english")
    mnemonic = 'legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful legal will'
    data = b'\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f\x7f'
    assert mnemonic == m.to_mnemonic(data)
    seed = libra.KeyFactory.to_seed(mnemonic)
    assert '8d8d9b85e36b2b9486becd31288e9dc2501cf77f95deb7d141eeb49d77f8a80f' == bytes.hex(seed)
    kfac = libra.KeyFactory(seed)
    master = bytes.hex(kfac.master)
    assert master == "16274c9618ed59177ca948529c1884ba65c57984d562ec2b4e5aa1ee3e3903be"
    child0 = kfac.private_child(0)
    assert bytes.hex(child0) == "358a375f36d74c30b7f3299b62d712b307725938f8cc931100fbd10a434fc8b9"
    child1 = kfac.private_child(1)
    assert bytes.hex(child1) == "a325fe7d27b1b49f191cc03525951fec41b6ffa2d4b3007bb1d9dd353b7e56a6"
    child0_again = kfac.private_child(0)
    assert child0_again == child0
    child1_again = kfac.private_child(1)
    assert child1_again == child1

def test_wallet():
    kfac = libra.KeyFactory.read_wallet_file('test/test.wallet')
    assert kfac.child_number == 2
    child0 = kfac.private_child(0)
    a0 = libra.Account(child0)
    assert a0.address_hex == "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e2f"
    assert a0.public_key_hex == "d1f4e85a3582015deb92d8aba35061a8032865d754a364d2429d475d10829c2a"
    assert a0.private_key_hex == "177bb836b2bb9be29f5accdf74a95d917946001282d7ee74b18d0c81764ee383"
    child1 = kfac.private_child(1)
    a1 = libra.Account(child1)
    assert a1.address_hex == "f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde"
    assert a1.public_key_hex == "6b72f3922ccbe671409c5ad0552f93888427f466ea0b7fdf3f066b31bce5c6a6"
    assert a1.private_key_hex == "2aa7e79ffe6bcb110b2a736ef4d37ad471c88b6f5be833cf1f2989ef12db05be"
