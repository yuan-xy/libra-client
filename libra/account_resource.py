from canoser import *
from libra.event import EventHandle
from libra.hasher import gen_hasher
from libra.account_config import AccountConfig
from io import StringIO

class AccountStateBlob:
    def __init__(self, blob):
        self.blob = blob

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.blob)

    def hash(self):
        shazer = gen_hasher(b"AccountStateBlob")
        shazer.update(self.blob)
        return shazer.digest()


class AccountState(Struct):
    _fields = [
        ('ordered_map', {})
    ]

    def __str__(self):
        concat = StringIO()
        concat.write(super().__str__())
        resource = self.ordered_map[AccountConfig.ACCOUNT_RESOURCE_PATH]
        ar = AccountResource.deserialize(resource)
        concat.write("\nDecoded:\n")
        concat.write(ar.__str__())
        return concat.getvalue()


class AccountResource(Struct):
    _fields = [
        ('authentication_key', [Uint8]),
        ('balance', Uint64),
        ('delegated_key_rotation_capability', bool),
        ('delegated_withdrawal_capability', bool),
        ('received_events', EventHandle),
        ('sent_events', EventHandle),
        ('sequence_number', Uint64)
    ]
