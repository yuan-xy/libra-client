import libra
from mnemonic import Mnemonic

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




