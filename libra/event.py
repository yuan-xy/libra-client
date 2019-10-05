from canoser import *
from libra.hasher import gen_hasher


EVENT_KEY_LENGTH = 32

class EventKey(DelegateT):
    delegate_type = [Uint8, EVENT_KEY_LENGTH]


class EventHandle(Struct):
    _fields = [
        ('count', Uint64),
        ('key', EventKey)
    ]


class ContractEvent(Struct):
    _fields = [
        ('key', EventKey),
        ('sequence_number', Uint64),
        ('event_data', [Uint8])
    ]

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.key = bytes_to_int_list(proto.key)
        ret.sequence_number = proto.sequence_number
        ret.event_data = bytes_to_int_list(proto.event_data)
        return ret

    def hash(self):
        shazer = gen_hasher(b"ContractEvent")
        shazer.update(self.serialize())
        return shazer.digest()
