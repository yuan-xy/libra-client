from canoser import Struct, Uint64
from libra.transaction import Version
from libra.hasher import HashValue
from libra.validator_set import ValidatorSet

# The delimiter between the version and the hash.
WAYPOINT_DELIMITER = ':'


class Waypoint(Struct):
    """
    # Waypoint keeps information about the LedgerInfo on a given reconfiguration, which provides an
    # off-chain mechanism to verify the sync process right after the restart.
    # At high level, a trusted waypoint verifies the LedgerInfo for a certain epoch change.
    # For more information, please refer to the Waypoints documentation.
    """
    _fields = [
        # The version of the reconfiguration transaction that is being approved by this waypoint.
        ("version", Version),
        # The hash of the chosen fields of LedgerInfo (including the next validator set).
        ("value", HashValue)
    ]

    @classmethod
    def new(cls, ledger_info):
        converter = Ledger2WaypointConverter.new(ledger_info)
        return cls(ledger_info.version, converter.hash())



class Ledger2WaypointConverter(Struct):
    """
    # Keeps the fields of LedgerInfo that are hashed for generating a waypoint.
    # Note that not all the fields of LedgerInfo are included: some consensus-related fields
    # might not be the same for all the participants.
    """
    _fields = [
        ("epoch", Uint64),
        ("root_hash", HashValue),
        ("version", Version),
        ("timestamp_usecs", Uint64),
        ("next_validator_set", ValidatorSet)
    ]

    @classmethod
    def new(cls, ledger_info):
        if ledger_info.next_validator_set is None:
            raise ValueError("Cannot create a waypoint without validator set")
        ret = cls()
        ret.epoch = ledger_info.epoch
        ret.root_hash = ledger_info.transaction_accumulator_hash
        ret.version = ledger_info.version
        ret.timestamp_usecs = ledger_info.timestamp_usecs
        ret.next_validator_set = ledger_info.next_validator_set
        return ret


    def hash(self):
        shazer = gen_hasher(b"Ledger2WaypointConverter::libra_types::waypoint")
        shazer.update(self.serialize())
        return shazer.digest()

