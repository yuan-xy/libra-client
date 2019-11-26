from canoser import DelegateT, Uint8, bytes_to_int_list
from libra.hasher import gen_hasher

import hashlib, random
from datetime import datetime

ADDRESS_LENGTH = 32
HEX_ADDRESS_LENGTH = ADDRESS_LENGTH * 2

class Address(DelegateT):
    delegate_type = [Uint8, ADDRESS_LENGTH, False]

    @classmethod
    def hash(cls, address):
        shazer = gen_hasher(b"AccountAddress::libra_types::account_address")
        shazer.update(address)
        return shazer.digest()

    @staticmethod
    def normalize_to_bytes(address):
        if isinstance(address, str):
            return strict_parse_address(address)
        if isinstance(address, list):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return bytes(address)
        if isinstance(address, bytes):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return address
        raise TypeError(f"Address: {address} has unknown type.")

    @staticmethod
    def normalize_to_int_list(address):
        if isinstance(address, list):
            if len(address) != ADDRESS_LENGTH:
                raise ValueError(f"{address} is not a valid address.")
            return address
        return bytes_to_int_list(Address.normalize_to_bytes(address))

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

def strict_parse_address(s: str) -> bytes:
    def strict_parse_address(s: str, orig_str: str) -> bytes:
        if len(s) < HEX_ADDRESS_LENGTH:
            raise ValueError(f"{orig_str} is not a valid address.")
        elif len(s) == HEX_ADDRESS_LENGTH:
            return bytes.fromhex(s)
        elif s[0:2] == '0x':
            return strict_parse_address(s[2:], orig_str)
        elif s[0]=="'" and s[-1]=="'":
            return strict_parse_address(s[1:-1], orig_str)
        elif s[0]=='"' and s[-1]=='"':
            return strict_parse_address(s[1:-1], orig_str)
        else:
            raise ValueError(f"{orig_str} is not a valid address.")
    return strict_parse_address(s, s)


def gen_random_address():
    hasher = hashlib.sha256()
    ran = random.random() + datetime.now().timestamp()
    hasher.update(ran.__str__().encode('utf-8'))
    return hasher.digest().hex()[0:64]
