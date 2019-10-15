from canoser import *
from libra.account_address import Address
from libra.language_storage import StructTag
from libra.account_config import AccountConfig
from libra.access_path import AccessPath


class VerifyError(Exception):
    pass

class ValidatorPublicKeys(Struct):
    _fields = [
        ('account_address', Address),
        ('consensus_public_key', [Uint8]),
        ('network_identity_public_key', [Uint8]), #TODO: X25519StaticPublicKey::to_bytes(&self.network_identity_public_key)[..])
        ('network_signing_public_key', [Uint8]) #only consensus_public_key exsits in consensus_peer.config
    ]

class ValidatorSet(DelegateT):
    delegate_type = [ValidatorPublicKeys]

    VALIDATOR_SET_MODULE_NAME = "ValidatorSet"
    VALIDATOR_SET_STRUCT_NAME = "T"

    @classmethod
    def validator_set_tag(cls) -> StructTag:
        return StructTag(
            hex_to_int_list(AccountConfig.core_code_address()),
            cls.VALIDATOR_SET_MODULE_NAME,
            cls.VALIDATOR_SET_STRUCT_NAME,
            []
        )

    @classmethod
    def validator_set_path(cls):
        return AccessPath.resource_access_vec(cls.validator_set_tag(), [])

    @classmethod
    def from_proto(cls, next_validator_set_proto):
        #TODO: validator_set change
        raise Exception("not implemented.")

class ValidatorVerifier:
    def __init__(self, validators):
        self.validators = validators
        if len(validators) == 0:
            self.quorum_size = 0
            #TODO: weighted voting
        else:
            self.quorum_size = len(validators) * 2 // 3 + 1

    def batch_verify_aggregated_signature(self, ledger_info_hash, signatures):
        self.check_num_of_signatures(signatures)
        self.check_keys(signatures)
        #TODO: PublicKey::batch_verify_signatures(&hash, keys_and_signatures)
        self.verify_aggregated_signature(ledger_info_hash, signatures);

    def check_num_of_signatures(self, signatures):
        num = len(signatures)
        if num < self.quorum_size:
            raise VerifyError(f"TooFewSignatures: {num} < {self.quorum_size}")
        if num > len(self.validators):
            raise VerifyError(f"TooManySignatures: {num} > {len(self.validators)}")

    def check_keys(self, signatures):
        for v_s_proto in signatures:
            validator_id = v_s_proto.validator_id
            if not validator_id in self.validators:
                raise VerifyError(f"UnknownAuthor: {validator_id}")

    def verify_aggregated_signature(self, ledger_info_hash, signatures):
        #TODO: why validate all? according to proto file, there are >2/3 nodes signing this correctly
        for v_s_proto in signatures:
            validator_id = v_s_proto.validator_id
            signature = v_s_proto.signature
            self.verify_signature(validator_id, ledger_info_hash, signature)

    def verify_signature(self, validator_id, ledger_info_hash, signature):
        vkey = self.validators[validator_id]
        if not vkey:
            raise VerifyError(f"UnknownAuthor: {validator_id}")
        vkey.verify(ledger_info_hash, signature)
