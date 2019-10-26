from canoser import *
from libra.validator_verifier import ValidatorSet
from libra.hasher import gen_hasher

Version = Uint64

class OptionValidatorSet(RustOptional):
    _type = ValidatorSet

class LedgerInfo(Struct):
    _fields = [
        ('version', Version),
        ('transaction_accumulator_hash', [Uint8]),
        ('consensus_data_hash', [Uint8]),
        ('consensus_block_id', [Uint8]),
        ('epoch', Uint64),
        ('timestamp_usecs', Uint64),
        ('next_validator_set', OptionValidatorSet)
    ]

    def hash(self):
        shazer = gen_hasher(b"LedgerInfo")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.version = proto.version
        ret.transaction_accumulator_hash = bytes_to_int_list(proto.transaction_accumulator_hash)
        ret.consensus_data_hash = bytes_to_int_list(proto.consensus_data_hash)
        ret.consensus_block_id = bytes_to_int_list(proto.consensus_block_id)
        ret.epoch = proto.epoch
        ret.timestamp_usecs = proto.timestamp_usecs
        if proto.HasField("next_validator_set"):
            vset = ValidatorSet.from_proto(proto.next_validator_set)
            ret.next_validator_set = OptionValidatorSet(vset)
        else:
            ret.next_validator_set = OptionValidatorSet(None)
        return ret

    @classmethod
    def _deprecated_from_proto_v2(cls, proto):
        ret = cls.__new__(cls)
        for k, v in proto.ListFields():
            assert getattr(proto, k.name) == v
            setattr(ret, k.name, v)
        return ret
