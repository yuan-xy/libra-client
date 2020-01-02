from canoser import Struct, Uint64, Uint8
from libra.crypto.ed25519 import ED25519_PUBLIC_KEY_LENGTH
from libra.account_address import Address


class VerifyError(Exception):
    pass


class ValidatorInfo(Struct):
    _fields = [
        ('public_key', [Uint8, ED25519_PUBLIC_KEY_LENGTH]),
        ('voting_power', Uint64)
    ]



class ValidatorVerifier(Struct):
    _fields = [
        ('address_to_validator_info', {Address: ValidatorInfo}),
        ('quorum_voting_power', Uint64),
        ('total_voting_power', Uint64)
    ]

    def __init__(self, address_to_validator_info):
        super().__init__(address_to_validator_info)
        self.total_voting_power = sum([v.voting_power for k,v in address_to_validator_info.items()])
        if len(address_to_validator_info) == 0:
            self.quorum_voting_power = 0
        else:
            self.quorum_voting_power = self.total_voting_power * 2 // 3 + 1

    @classmethod
    def from_validator_set(cls, vset):
        address_to_validator_info = {}
        for vpkeys in vset:
            vinfo = ValidatorInfo(vpkeys.consensus_public_key, vpkeys.consensus_voting_power)
            address_to_validator_info[bytes(vpkeys.account_address)] = vinfo
        return cls(address_to_validator_info)


    def batch_verify_aggregated_signature(self, ledger_info_hash, signatures):
        # TODO: update to support voting
        return
        self.check_num_of_signatures(signatures)
        self.check_keys(signatures)
        #TODO: PublicKey::batch_verify_signatures(&hash, keys_and_signatures)
        self.verify_aggregated_signature(ledger_info_hash, signatures);

    def check_num_of_signatures(self, signatures):
        num = len(signatures)
        if num < self.quorum_size:
            raise VerifyError(f"TooFewSignatures: {num} < {self.quorum_size}")
        if num > len(self.address_to_validator_info):
            raise VerifyError(f"TooManySignatures: {num} > {len(self.address_to_validator_info)}")

    def check_keys(self, signatures):
        for v_s_proto in signatures:
            validator_id = v_s_proto.validator_id
            if not validator_id in self.address_to_validator_info:
                raise VerifyError(f"UnknownAuthor: {validator_id}")

    def verify_aggregated_signature(self, ledger_info_hash, signatures):
        #TODO: why validate all? according to proto file, there are >2/3 nodes signing this correctly
        for v_s_proto in signatures:
            validator_id = v_s_proto.validator_id
            signature = v_s_proto.signature
            self.verify_signature(validator_id, ledger_info_hash, signature)

    def verify_signature(self, validator_id, ledger_info_hash, signature):
        vkey = self.address_to_validator_info[validator_id]
        if not vkey:
            raise VerifyError(f"UnknownAuthor: {validator_id}")
        vkey.verify(ledger_info_hash, signature)
