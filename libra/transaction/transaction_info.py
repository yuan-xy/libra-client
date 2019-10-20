from canoser import Struct, bytes_to_int_list, Uint64
from libra.hasher import gen_hasher, HashValue
from libra.access_path import AccessPath


class TransactionInfo(Struct):
    _fields = [
        ('signed_transaction_hash', HashValue),
        ('state_root_hash', HashValue),
        ('event_root_hash', HashValue),
        ('gas_used', Uint64),
        ('major_status', Uint64)
    ]

    def hash(self):
        shazer = gen_hasher(b"TransactionInfo")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.signed_transaction_hash = bytes_to_int_list(proto.signed_transaction_hash)
        ret.state_root_hash = bytes_to_int_list(proto.state_root_hash)
        ret.event_root_hash = bytes_to_int_list(proto.event_root_hash)
        ret.gas_used = proto.gas_used
        ret.major_status = proto.major_status
        return ret
