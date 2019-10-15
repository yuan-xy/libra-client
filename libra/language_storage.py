from canoser import Struct
from libra.account_address import Address
from libra.identifier import Identifier
from libra.hasher import gen_hasher


class StructTag(Struct):
    _fields = [
        ('address', Address),
        ('module', Identifier),
        ('name', Identifier),
        ('type_params', ['libra.language_storage.StructTag'])
    ]

    def hash(self):
        shazer = gen_hasher(b"VM_ACCESS_PATH")
        shazer.update(self.serialize())
        return shazer.digest()


# Represents the intitial key into global storage where we first index by the address, and then
# the struct tag
class ResourceKey(Struct):
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
        shazer = gen_hasher(b"VM_ACCESS_PATH")
        shazer.update(self.serialize())
        return shazer.digest()
