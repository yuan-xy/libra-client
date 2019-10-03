from canoser import *
from libra.account_address import Address

class ValidatorPublicKeys(Struct):
    _fields = [
        ('account_address', Address),
        ('consensus_public_key', [Uint8]),
        ('network_identity_public_key', [Uint8]), #TODO: X25519StaticPublicKey::to_bytes(&self.network_identity_public_key)[..])
        ('network_signing_public_key', [Uint8]) #only consensus_public_key exsits in consensus_peer.config
    ]

class ValidatorSet(DelegateT):
    delegate_type = [ValidatorPublicKeys]

class ValidatorVerifier:
    def __init__(self, validators):
        self.validators = validators
        if len(validators) == 0:
            self.quorum_size = 0
        else:
            self.quorum_size = len(validators) * 2 // 3 + 1

    def batch_verify_aggregated_signature(self, ledger_info_hash, signatures):
        pass