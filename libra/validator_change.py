from canoser import RustEnum
from typing import List
from libra.ledger_info import LedgerInfoWithSignatures

# A vector of LedgerInfo with contiguous increasing epoch numbers to prove a sequence of
# validator changes from the first LedgerInfo's epoch.
class ValidatorChangeProof:
    # pub ledger_info_with_sigs: Vec<LedgerInfoWithSignatures>,
    # pub more: bool,
    def __init__(self, ledger_info_with_sigs : List(LedgerInfoWithSignatures), more : bool):
        self.ledger_info_with_sigs = ledger_info_with_sigs
        self.more = more



class VerifierType(RustEnum):
    """
    # The verification of the validator change proof starts with some verifier that is trusted by the
    # client: could be either a waypoint (upon startup) or a known validator verifier.
    """
    _enums = [
        ('Waypoint', Waypoint),
        ('TrustedVerifier', EpochInfo)
    ]
