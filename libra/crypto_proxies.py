from canoser import Struct, Uint64
from libra.validator_verifier import ValidatorVerifier

# EpochInfo represents a trusted validator set to validate messages from the specific epoch,
# it could be updated with ValidatorChangeProof.
class EpochInfo(Struct):
    _fields = [
        ('epoch', Uint64),
        ('verifier', ValidatorVerifier)
    ]

    @classmethod
    def empty(cls):
        ret = cls(0, ValidatorVerifier({}))
        return ret

