from libra.ledger_info import LedgerInfo
from libra.validator_verifier import VerifyError
from libra.hasher import *
from libra.proof import verify_transaction_list
from libra.proof.signed_transaction_with_proof import SignedTransactionWithProof
from libra.proof.account_state_with_proof import AccountStateWithProof
from libra.proof.event_with_proof import EventWithProof
from libra.transaction import SignedTransaction, TransactionInfo
from libra.account_address import Address
from libra.proof import ensure, bail
from libra.account_resource import AccountResource
import canoser


def verify(validator_verifier, request, response):
    verify_update_to_latest_ledger_response(
        validator_verifier,
        request.client_known_version,
        request.requested_items,
        response.response_items,
        response.ledger_info_with_sigs
    )

def verify_update_to_latest_ledger_response(
    validator_verifier,
    req_client_known_version,
    requested_items,
    response_items,
    ledger_info_with_sigs
    ):
    ledger_info_proto = ledger_info_with_sigs.ledger_info
    ledger_info = LedgerInfo.from_proto(ledger_info_proto)
    signatures = ledger_info_with_sigs.signatures
    if ledger_info.version < req_client_known_version:
        raise VerifyError(f"ledger_info.version:{ledger_info.version} < {req_client_known_version}.")
    if ledger_info.version > 0 or signatures.__len__() > 0:
        validator_verifier.batch_verify_aggregated_signature(ledger_info.hash(), signatures)
    if len(response_items) != len(requested_items):
        raise VerifyError(f"{len(response_items)} != {len(requested_items)}")
    for req_item, resp_item in zip(requested_items, response_items):
        verify_response_item(ledger_info, req_item, resp_item)

def verify_response_item(ledger_info, requested_item, response_item):
    req_type = requested_item.WhichOneof('requested_items')
    if not req_type.endswith("_request"):
        raise VerifyError(f"RequestItem type unknown{req_type}.")
    resp_type = req_type.replace("_request", "_response")
    resp_type2 = response_item.WhichOneof('response_items')
    if resp_type != resp_type2:
        raise VerifyError(f"RequestItem/ResponseItem types mismatch:{resp_type} - {resp_type2}.")
    if resp_type == "get_account_state_response":
        asp = response_item.get_account_state_response.account_state_with_proof
        AccountStateWithProof.verify(asp, ledger_info, ledger_info.version,
            requested_item.get_account_state_request.address)
    elif resp_type == "get_account_transaction_by_sequence_number_response":
        atreq = requested_item.get_account_transaction_by_sequence_number_request
        atresp = response_item.get_account_transaction_by_sequence_number_response
        verify_get_txn_by_seq_num_resp(
            ledger_info,
            atreq.account,
            atreq.sequence_number,
            atreq.fetch_events,
            atresp.signed_transaction_with_proof,
            atresp.proof_of_current_sequence_number
        )
    elif resp_type == "get_events_by_event_access_path_response":
        ereq = requested_item.get_events_by_event_access_path_request
        eresp = response_item.get_events_by_event_access_path_response
        verify_get_events_by_access_path_resp(
            ledger_info,
            ereq.access_path,
            ereq.start_event_seq_num,
            ereq.ascending,
            ereq.limit,
            eresp.events_with_proof,
            eresp.proof_of_latest_event
        )
    elif resp_type == "get_transactions_response":
        req = requested_item.get_transactions_request
        ver = req.start_version
        limit = req.limit
        fetch_events = req.fetch_events
        txp = response_item.get_transactions_response.txn_list_with_proof
        verify_get_txns_resp(ledger_info, ver, limit, fetch_events, txp)
    else:
        raise VerifyError(f"unknown response type:{resp_type}")


def verify_get_txn_by_seq_num_resp(
        ledger_info,
        account,
        sequence_number,
        fetch_events,
        signed_transaction_with_proof,
        proof_of_current_sequence_number
    ):
    has_stx = len(signed_transaction_with_proof.__str__()) > 0
    has_cur = len(proof_of_current_sequence_number.__str__()) > 0
    if has_stx and not has_cur:
        ensure(
            fetch_events == signed_transaction_with_proof.HasField("events"),
            "Bad GetAccountTxnBySeqNum response. Events requested: {}, events returned: {}.",
            fetch_events,
            signed_transaction_with_proof.HasField("events")
        )
        SignedTransactionWithProof.verify(
            signed_transaction_with_proof,
            ledger_info,
            signed_transaction_with_proof.version,
            account,
            sequence_number
        )
    elif has_cur and not has_stx:
        sequence_number_in_ledger = AccountResource.get_account_resource_or_default(
            proof_of_current_sequence_number.blob).sequence_number
        ensure(
            sequence_number_in_ledger <= sequence_number,
            "Server returned no transactions while it should. Seq num requested: {}, latest seq num in ledger: {}.",
            sequence_number,
            sequence_number_in_ledger
        )
        AccountStateWithProof.verify(proof_of_current_sequence_number, ledger_info,
            ledger_info.version, account)
    else:
        bail(
            "Bad GetAccountTxnBySeqNum response. txn_proof.is_none():{}, cur_seq_num_proof.is_none():{}",
            has_stx,
            has_cur
        )




def verify_get_events_by_access_path_resp(
        ledger_info,
        req_access_path,
        req_start_seq_num,
        req_ascending,
        req_limit,
        events_with_proof,
        proof_of_latest_event,
    ):
    account_resource = AccountResource.get_account_resource_or_default(proof_of_latest_event.blob)
    AccountStateWithProof.verify(proof_of_latest_event, ledger_info, ledger_info.version,
            req_access_path.address)
    event_handle = account_resource.get_event_handle_by_query_path(req_access_path.path)
    expected_event_key = event_handle.key
    expected_seq_nums = gen_events_resp_idxs(event_handle.count,
        req_start_seq_num, req_ascending, req_limit)
    ensure(
        len(expected_seq_nums) == len(events_with_proof),
        "Expecting {} events, got {}.",
        len(expected_seq_nums),
        len(events_with_proof)
    )
    zipped = zip(events_with_proof, expected_seq_nums)
    for event_with_proof, seq_num in zipped:
        EventWithProof.verify(
            event_with_proof,
            ledger_info,
            expected_event_key,
            seq_num,
            event_with_proof.transaction_version,
            event_with_proof.event_index
        )


def gen_events_resp_idxs(seq_num_upper_bound, req_start_seq_num, req_ascending, req_limit):
    if not req_ascending and req_start_seq_num == canoser.Uint64.max_value and seq_num_upper_bound > 0:
        cursor = seq_num_upper_bound - 1
    else:
        cursor = req_start_seq_num
    if cursor >= seq_num_upper_bound:
        return [] #Unreachable, so empty.
    elif req_ascending:
        #Ascending, from start to upper bound or limit.
        realupper = min(cursor + req_limit, seq_num_upper_bound)
        return [x for x in range(cursor, realupper)]
    elif cursor + 1 < req_limit:
        return [x for x in range(cursor, -1, -1)] # Descending and hitting 0.
    else:
        bottom = cursor + 1 - req_limit
        return [x for x in range(cursor, bottom-1, -1)] #Descending and hitting limit.


def verify_get_txns_resp(ledger_info, start_version, limit, fetch_events, txn_list_with_proof):
    if limit == 0 or start_version > ledger_info.version:
        if txn_list_with_proof.SerializeToString() != b'':
            raise VerifyError(f"transactions should be empty.")
        return
    if fetch_events != txn_list_with_proof.HasField("events_for_versions"):
        raise VerifyError(f"fetch_events: {fetch_events} mismatch with events_for_versions")
    num_txns = len(txn_list_with_proof.transactions)
    ret_num = min(limit, ledger_info.version - start_version + 1)
    if num_txns != ret_num:
        raise VerifyError(f"transaction number expected:{ret_num}, returned:{num_txns}.")
    verify_start_version(txn_list_with_proof, start_version)
    verify_transaction_list(txn_list_with_proof, ledger_info)

def verify_start_version(txn_list_with_proof, start_version):
    ver = txn_list_with_proof.first_transaction_version.value
    if ver != start_version:
        raise VerifyError(f"transaction version mismatch:{start_version}, returned:{ver}.")
