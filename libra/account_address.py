from canoser import DelegateT, Uint8
from libra.hasher import gen_hasher


ADDRESS_LENGTH = 32
HEX_ADDRESS_LENGTH = ADDRESS_LENGTH * 2

class Address(DelegateT):
    delegate_type = [Uint8, ADDRESS_LENGTH]

    @classmethod
    def hash(cls, address):
        shazer = gen_hasher(b"AccountAddress")
        shazer.update(address)
        return shazer.digest()

def parse_address(s: str) -> bytes:
    if s[0:2] == '0x':
        s = s[2:]
        if len(s) < HEX_ADDRESS_LENGTH:
            s = s.rjust(HEX_ADDRESS_LENGTH, '0')
    if len(s) == HEX_ADDRESS_LENGTH:
        return bytes.fromhex(s)
    return None