from canoser import Struct, Uint8
from libra.account_address import Address

class AccessPath(Struct):
    _fields = [
        ('address', Address),
        ('path', [Uint8])
    ]