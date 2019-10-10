from libra.proof import ensure, bail, verify_accumulator_element, verify_transaction_info
from libra.event import ContractEvent
from libra.hasher import EventAccumulatorHasher

class EventWithProof:
    # Two things are ensured if no error is raised:
    #   1. This event exists in the ledger represented by `ledger_info`.
    #   2. And this event has the same `event_key`, `sequence_number`, `transaction_version`,
    # and `event_index` as indicated in the parameter list. If any of these parameter is unknown
    # to the call site and is supposed to be informed by this struct, get it from the struct
    # itself, such as: `event_with_proof.event.access_path()`, `event_with_proof.event_index()`,
    # etc.
    @classmethod
    def verify(
            cls,
            event_with_proof,
            ledger_info,
            event_key,
            sequence_number,
            transaction_version,
            event_index):
        ensure(
            event_with_proof.event.key == bytes(event_key),
            "Event key ({}) not expected ({}).",
            event_with_proof.event.key,
            bytes(event_key)
        )
        ensure(
            event_with_proof.event.sequence_number == sequence_number,
            "Sequence number ({}) not expected ({}).",
            event_with_proof.event.sequence_number,
            sequence_number
        )
        ensure(
            event_with_proof.transaction_version == transaction_version,
            "Transaction version ({}) not expected ({}).",
            event_with_proof.transaction_version,
            transaction_version
        )
        ensure(
            event_with_proof.event_index == event_index,
            "Event index ({}) not expected ({}).",
            event_with_proof.event_index,
            event_index
        )
        ce = ContractEvent.from_proto(event_with_proof.event)
        verify_event(
            ledger_info,
            ce.hash(),
            transaction_version,
            event_index,
            event_with_proof.proof
        )

def verify_event(
            ledger_info,
            event_hash,
            transaction_version,
            event_version_within_transaction,
            event_proof
        ):
    verify_accumulator_element(
        EventAccumulatorHasher,
        event_proof.transaction_info.event_root_hash,
        event_hash,
        event_version_within_transaction,
        event_proof.transaction_info_to_event_proof
    )
    verify_transaction_info(
        ledger_info,
        transaction_version,
        event_proof.transaction_info,
        event_proof.ledger_info_to_transaction_info_proof
    )
