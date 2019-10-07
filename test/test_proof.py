import libra
from libra.transaction import TransactionInfo
from libra.hasher import TransactionAccumulatorHasher
from libra.proof import *
import pytest
import pdb

def test_merkle_tree_accumulator_invariants():
    c = libra.Client("testnet")
    request, resp = c._get_txs(1, 2, False)
    version = resp.ledger_info_with_sigs.ledger_info.version
    txn_list = resp.response_items[0].get_transactions_response.txn_list_with_proof
    first = txn_list.proof_of_first_transaction.non_default_siblings
    last = txn_list.proof_of_last_transaction.non_default_siblings
    assert len(first) == len(last)
    assert 2**len(first) > version
    assert 2**(len(first)-1) < version
    common = 0
    for v1, v2 in zip(first, last):
        if v1 == v2:
            common += 1
        else:
            break
    assert len(first) - common == 2
    hash1 = TransactionInfo.from_proto(txn_list.infos[0]).hash()
    hash0 = first[-1]
    hasher = TransactionAccumulatorHasher()
    hash01 = MerkleTreeInternalNode(hash0, hash1, hasher).hash()
    assert hash01 == last[-2]
    hash2 = TransactionInfo.from_proto(txn_list.infos[1]).hash()
    hash3 = last[-1]
    hasher = TransactionAccumulatorHasher()
    hash23 = MerkleTreeInternalNode(hash2, hash3, hasher).hash()
    assert hash23 == first[-2]
    root_hash = hash01
    for item in reversed(first[0:-1]):
        hasher = TransactionAccumulatorHasher()
        root_hash = MerkleTreeInternalNode(root_hash, item, hasher).hash()
    assert root_hash == resp.ledger_info_with_sigs.ledger_info.transaction_accumulator_hash
    #TODO: test bitmap

def test_ensure():
    ensure(1==1, "{} != {}", 1, 1)
    with pytest.raises(AssertionError):
        ensure(1==2, "{} != {}", 1, 2)
    with pytest.raises(AssertionError):
        ensure(1==2, "1 != 2")