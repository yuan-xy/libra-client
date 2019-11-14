from libra.language_storage import *
from canoser import Uint32
#import pdb


def test_struct_tag():
    tag1 = StructTag([1]*32, 'm1', 'n1', [])
    tag2 = StructTag([2]*32, 'm2', 'n2', [])
    tag3 = StructTag([3]*32, 'm3', 'n3', [tag1, tag2])
    tag1s = tag1.serialize()
    tag2s = tag2.serialize()
    arrs = Uint32.encode(2)+ tag1s + tag2s
    tag3s = tag3.serialize()
    assert tag3s.endswith(arrs)
    assert StructTag.deserialize(tag3s) == tag3