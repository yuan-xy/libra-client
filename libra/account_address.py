from canoser import DelegateT, Uint8
from libra.hasher import gen_hasher


ADDRESS_LENGTH = 32

class Address(DelegateT):
    delegate_type = [Uint8, ADDRESS_LENGTH]

    @classmethod
    def hash(cls, address):
        shazer = gen_hasher(b"AccountAddress")
        shazer.update(address)
        return shazer.digest()