import libra
from mnemonic import Mnemonic
from nacl.signing import SigningKey
from libra.key_factory import has_sha3

import pdb

def test_key():
    if not has_sha3():
        return
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

