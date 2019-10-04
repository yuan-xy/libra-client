from libra.ledger_info import LedgerInfo
from libra.validator_verifier import VerifyError
from libra.hasher import *
from libra.event import ContractEvent
from libra.proof import get_accumulator_root_hash
from libra.transaction import SignedTransaction, TransactionInfo

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
    if resp_type == "get_transactions_response":
        req = requested_item.get_transactions_request
        ver = req.start_version
        limit = req.limit
        fetch_events = req.fetch_events
        txp = response_item.get_transactions_response.txn_list_with_proof
        verify_get_txns_resp(ledger_info, ver, limit, fetch_events, txp)




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

def verify_transaction_list(txn_list_with_proof, ledger_info):
    #TODO: all transactions should be same epoch
    transactions = txn_list_with_proof.transactions
    infos = txn_list_with_proof.infos
    len_tx = len(transactions)
    len_info = len(infos)
    if len_tx != len_info:
        raise VerifyError(f"transactions and infos mismatch:{len_tx}, {len_info}.")
    if txn_list_with_proof.HasField("events_for_versions"):
        event_lists = txn_list_with_proof.events_for_versions.events_for_version
        verify_event_root_hash(event_lists, infos)
    #Get the hashes of all nodes at the accumulator leaf level.
    zipped = zip(txn_list_with_proof.transactions, txn_list_with_proof.infos)
    for tx, info in zipped:
        stx = SignedTransaction.from_proto(tx)
        if stx.hash() != info.signed_transaction_hash:
            raise VerifyError(f"transaction hash mismatch:{stx}.")
    # import pdb
    # pdb.set_trace()
    hashes = [TransactionInfo.from_proto(x).hash() for x in infos]

#Verify event root hashes match what is carried on the transaction infos.
def verify_event_root_hash(event_lists, infos):
    len_event = len(event_lists)
    len_info = len(infos)
    if len_info != len_event:
        raise VerifyError(f"transactions and events mismatch:{len_info}, {len_event}.")
    zipped = zip(event_lists, infos)
    for events, info in zipped:
        event_hashes = [ContractEvent.from_proto(x).hash() for x in events.events]
        eroot_hash = get_accumulator_root_hash(EventAccumulatorHasher(), event_hashes)
        if eroot_hash != info.event_root_hash:
            raise VerifyError(f"event_root_hash mismatch.")