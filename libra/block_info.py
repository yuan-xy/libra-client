from canoser import Struct, RustOptional, Uint64
from libra.transaction import Version
from libra.hasher import HashValue
from libra.validator_set import ValidatorSet

# The round of a block is a consensus-internal counter, which starts with 0 and increases
# monotonically.
Round = Uint64


class OptionValidatorSet(RustOptional):
    _type = ValidatorSet


class BlockInfo(Struct):
    """
    # This structure contains all the information needed for tracking a block
    # without having access to the block or its execution output state. It
    # assumes that the block is the last block executed within the ledger.
    """
    _fields = [
        # Epoch number corresponds to the set of validators that are active for this block.
        ("epoch", Uint64),
        # The consensus protocol is executed in rounds, which monotonically increase per epoch.
        ("round", Round),
        # The identifier (hash) of the block.
        ("id", HashValue),
        # The accumulator root hash after executing this block.
        ("executed_state_id", HashValue),
        # The version of the latest transaction after executing this block.
        ("version", Version),
        # The timestamp this block was proposed by a proposer.
        ("timestamp_usecs", Uint64),
        # An optional field containing the set of validators for the start of the next epoch
        ("next_validator_set", OptionValidatorSet)
    ]


