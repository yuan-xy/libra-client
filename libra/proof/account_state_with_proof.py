from libra.account_address import Address
from libra.proof import ensure, bail, verify_sparse_merkle_element, verify_transaction_info


class AccountStateWithProof:
    @classmethod
    def verify(
            cls,
            account_state_proof,
            ledger_info,
            version,
            address
        ):
        ensure(
            account_state_proof.version == version,
            "State version ({}) is not expected ({}).",
            account_state_proof.version,
            version
        )
        verify_account_state(
            ledger_info,
            version,
            Address.hash(address),
            account_state_proof.blob,
            account_state_proof.proof
        )

# Verifies that the state of an account at version `state_version` is correct using the provided
# proof.  If `account_state_blob` is present, we expect the account to exist, otherwise we
# expect the account to not exist.
def verify_account_state(
        ledger_info,
        state_version,
        account_address_hash,
        account_state_blob,
        account_state_proof
        ):
    verify_sparse_merkle_element(
        account_state_proof.transaction_info.state_root_hash,
        account_address_hash,
        account_state_blob,
        account_state_proof.transaction_info_to_account_proof
    )
    verify_transaction_info(
        ledger_info,
        state_version,
        account_state_proof.transaction_info,
        account_state_proof.ledger_info_to_transaction_info_proof)

