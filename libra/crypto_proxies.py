from canoser import Struct, Uint64
from libra.validator_verifier import ValidatorVerifier

# EpochInfo represents a trusted validator set to validate messages from the specific epoch,
# it could be updated with ValidatorChangeProof.
class EpochInfo:
    def __init__(self, epoch : Uint64, verifier : ValidatorVerifier):
        self.epoch = epoch
        self.verifier = verifier
