from canoser import Struct, Uint8, Uint64, bytes_to_int_list
from libra.account_address import Address

class ValidatorPublicKeys(Struct):
    _fields = [
        ('account_address', Address),
        ('consensus_public_key', [Uint8]),
        ('consensus_voting_power', Uint64),
        ('network_signing_public_key', [Uint8]),
        ('network_identity_public_key', [Uint8])
    ]

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.account_address = bytes_to_int_list(proto.account_address)
        ret.consensus_public_key = bytes_to_int_list(proto.consensus_public_key)
        ret.consensus_voting_power = proto.consensus_voting_power
        ret.network_signing_public_key = bytes_to_int_list(proto.network_signing_public_key)
        ret.network_identity_public_key = bytes_to_int_list(proto.network_identity_public_key)
        return ret
