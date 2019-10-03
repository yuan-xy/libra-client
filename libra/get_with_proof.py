from libra.ledger_info import LedgerInfo

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
    assert ledger_info.version >= req_client_known_version
    if ledger_info.version > 0 or signatures.__len__() > 0:
        validator_verifier.batch_verify_aggregated_signature(ledger_info.hash(), signatures)
    assert len(response_items) == len(requested_items)
    for req_item, resp_item in zip(requested_items, response_items):
        verify_response_item(ledger_info, req_item, resp_item)

def verify_response_item(ledger_info, requested_item, response_item):
    pass
