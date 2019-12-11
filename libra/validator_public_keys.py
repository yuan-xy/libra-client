from canoser import Struct, Uint8
from libra.account_address import Address

class ValidatorPublicKeys(Struct):
    _fields = [
        ('account_address', Address),
        ('consensus_public_key', [Uint8]),
        ('network_identity_public_key', [Uint8]), #TODO: X25519StaticPublicKey::to_bytes(&self.network_identity_public_key)[..])
        ('network_signing_public_key', [Uint8]) #only consensus_public_key exsits in consensus_peer.config
    ]