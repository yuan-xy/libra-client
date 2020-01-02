from canoser import Struct, Uint8, bytes_to_int_list
from libra.account_address import Address
from libra.block_info import BlockInfo, OptionValidatorSet
from libra.hasher import HashValue, gen_hasher
from libra.crypto.ed25519 import ED25519_SIGNATURE_LENGTH
from libra.validator_set import ValidatorSet
from libra.validator_verifier import ValidatorVerifier

class LedgerInfo(Struct):

    _fields = [
        ('commit_info', BlockInfo),
        # Hash of consensus specific data that is opaque to all parts of the system other than
        # consensus.
        ('consensus_data_hash', HashValue)
    ]

    def hash(self):
        shazer = gen_hasher(b"LedgerInfo::libra_types::ledger_info")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        block_info = BlockInfo()
        block_info.version = proto.version
        block_info.executed_state_id = bytes_to_int_list(proto.transaction_accumulator_hash)
        block_info.id = bytes_to_int_list(proto.consensus_block_id)
        block_info.epoch = proto.epoch
        block_info.round = proto.round
        block_info.timestamp_usecs = proto.timestamp_usecs
        if proto.HasField("next_validator_set"):
            vset = ValidatorSet.from_proto(proto.next_validator_set)
            block_info.next_validator_set = OptionValidatorSet(vset)
        else:
            block_info.next_validator_set = OptionValidatorSet(None)
        ret.commit_info = block_info
        ret.consensus_data_hash = bytes_to_int_list(proto.consensus_data_hash)
        return ret

    @property
    def epoch(self):
        return self.commit_info.epoch

    @property
    def round(self):
        return self.commit_info.round

    @property
    def consensus_block_id(self):
        return self.commit_info.id

    @property
    def transaction_accumulator_hash(self):
        return self.commit_info.executed_state_id

    @property
    def version(self):
        return self.commit_info.version

    @property
    def timestamp_usecs(self):
        return self.commit_info.timestamp_usecs

    @property
    def next_validator_set(self):
        return self.commit_info.next_validator_set

    def has_next_validator_set(self):
        return self.commit_info.next_validator_set.value is not None



# The validator node returns this structure which includes signatures
# from validators that confirm the state.  The client needs to only pass back
# the LedgerInfo element since the validator node doesn't need to know the signatures
# again when the client performs a query, those are only there for the client
# to be able to verify the state
class LedgerInfoWithSignatures(Struct):

    _fields = [
        ('ledger_info', LedgerInfo),
        # The validator is identified by its account address: in order to verify a signature
        # one needs to retrieve the public key of the validator for the given epoch.
        ('signatures', {Address: [Uint8, ED25519_SIGNATURE_LENGTH]})
    ]

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.ledger_info = LedgerInfo.from_proto(proto.ledger_info)
        signatures = {}
        for x in proto.signatures:
            #address = Address.normalize_to_bytes(x.validator_id)
            signatures[x.validator_id] = bytes_to_int_list(x.signature)
        ret.signatures = signatures
        return ret

    def verify(self, validator: ValidatorVerifier):
        ledger_hash = self.ledger_info.hash()
        validator.batch_verify_aggregated_signature(ledger_hash, self.signatures)

