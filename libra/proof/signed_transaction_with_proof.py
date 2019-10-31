from libra.hasher import *
from libra.proof import ensure, bail, verify_transaction_info
from libra.transaction import SignedTransaction, TransactionInfo
from libra.proof.merkle_tree import get_event_root_hash

class SignedTransactionWithProof:
    @classmethod
    def verify(
            cls,
            signed_transaction_with_proof,
            ledger_info,
            version,
            sender,
            sequence_number
        ):
        stx = SignedTransaction.deserialize(signed_transaction_with_proof.signed_transaction.txn_bytes)
        #TODO: avoid duplicated deserialize.
        ensure(
            signed_transaction_with_proof.version == version,
            "Version ({}) is not expected ({}).",
            signed_transaction_with_proof.version,
            version
        )
        ensure(
            bytes(stx.sender) == sender,
            "Sender ({}) not expected ({}).",
            bytes(stx.sender),
            sender
        )
        ensure(
            stx.sequence_number == sequence_number,
            "Sequence number ({}) not expected ({}).",
            stx.sequence_number,
            sequence_number
        )
        if signed_transaction_with_proof.HasField("events"):
            events_root_hash = get_event_root_hash(signed_transaction_with_proof.events.events)
        else:
            events_root_hash = None
        verify_signed_transaction(
            ledger_info,
            stx.hash(),
            events_root_hash,
            version,
            signed_transaction_with_proof.proof
        )



# Verifies that a `SignedTransaction` with hash value of `transaction_hash`
# is the version `transaction_version` transaction in the ledger using the provided proof.
# If event_root_hash is provided, it's also verified against the proof.
def verify_signed_transaction(
        ledger_info,
        transaction_hash,
        event_root_hash,
        transaction_version,
        signed_transaction_proof
    ):
    transaction_info = TransactionInfo.from_proto(signed_transaction_proof.transaction_info)
    ensure(
        transaction_hash == bytes(transaction_info.transaction_hash),
        "The hash of signed transaction does not match the transaction info in proof. \
         Transaction hash: {}. Transaction hash provided by proof: {}.",
        transaction_hash,
        bytes(transaction_info.transaction_hash)
    )
    if event_root_hash is not None:
        ensure(
            bytes(event_root_hash) == bytes(transaction_info.event_root_hash),
            "Event root hash ({}) doesn't match that in the transaction info ({}).",
            bytes(event_root_hash),
            bytes(transaction_info.event_root_hash)
        )
    verify_transaction_info(
        ledger_info,
        transaction_version,
        transaction_info,
        signed_transaction_proof.ledger_info_to_transaction_info_proof
    )