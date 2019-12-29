from canoser import Struct, RustEnum, Uint64, Uint8, Uint128
from libra.account_address import Address
from libra.identifier import Identifier
from libra.hasher import gen_hasher
import libra

class StructTag(Struct):
    _fields = [
        ('address', Address),
        ('module', Identifier),
        ('name', Identifier),
        ('type_params', ['libra.language_storage.StructTag'])
    ]

    def hash(self):
        shazer = gen_hasher(b"StructTag::libra_types::language_storage")
        shazer.update(self.serialize())
        return shazer.digest()

    def is_pay_tag(self):
        return self.address == libra.AccountConfig.core_code_address_ints() and\
                self.module == libra.AccountConfig.ACCOUNT_MODULE_NAME and\
                (self.name == "SentPaymentEvent" or self.name == "ReceivedPaymentEvent")


class TypeTag(RustEnum):
    _enums = [
        ('Bool', bool),
        ('U8', Uint8),
        ('U64', Uint64),
        ('U128', Uint128),
        ('ByteArray', [Uint8]),
        ('Address', Address),
        ('Struct', StructTag)
    ]



class ResourceKey(Struct):
    """Represents the intitial key into global storage where we first index by the address, and then the struct tag"""
    _fields = [
        ('address', Address),
        ('type_', StructTag)
    ]


class ModuleId(Struct):
    _fields = [
        ('address', Address),
        ('name', Identifier)
    ]

    def hash(self):
        shazer = gen_hasher(b"ModuleId::libra_types::language_storage")
        shazer.update(self.serialize())
        return shazer.digest()
