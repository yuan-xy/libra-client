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

    @staticmethod
    def normalize_to_bytes(address):
        if isinstance(address, str):
            return bytes.fromhex(address)
        if isinstance(address, list):
            return bytes(address)
        if isinstance(address, bytes):
            return address
        raise TypeError(f"Address: {address} has unknown type.")

    @staticmethod
    def equal_address(addr1, addr2):
        return Address.normalize_to_bytes(addr1) == Address.normalize_to_bytes(addr2)


def parse_address(s: str) -> bytes:
    if s[0:2] == '0x':
        s = s[2:]
        if len(s) < HEX_ADDRESS_LENGTH:
            s = s.rjust(HEX_ADDRESS_LENGTH, '0')
    if len(s) == HEX_ADDRESS_LENGTH:
        return bytes.fromhex(s)
    return None
