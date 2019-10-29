from libra.proof.merkle_tree import (get_event_root_hash,
    MerkleTreeInternalNode, SparseMerkleLeafNode)
from libra.proof.definition import AccumulatorProof, SparseMerkleProof, MAX_ACCUMULATOR_PROOF_DEPTH
from libra.hasher import *
from libra.transaction import SignedTransaction, TransactionInfo
from libra.account_resource import AccountStateBlob
from libra.validator_verifier import VerifyError

import collections
import more_itertools
import pdb


def bail(hint, *args):
    errstr = hint.format(*args)
    raise AssertionError(errstr)

def ensure(exp, hint, *args):
    if not exp:
        bail(hint, *args)

# Verifies that a given `transaction_info` exists in the ledger using provided proof.
def verify_transaction_info(
        ledger_info,
        transaction_version,
        transaction_info,
        ledger_info_to_transaction_info_proof):
    assert transaction_version <= ledger_info.version
    if not isinstance(transaction_info, TransactionInfo):
        transaction_info = TransactionInfo.from_proto(transaction_info)
    verify_accumulator_element(
        TransactionAccumulatorHasher,
        ledger_info.transaction_accumulator_hash,
        transaction_info.hash(),
        transaction_version,
        ledger_info_to_transaction_info_proof)



# Verifies an element whose hash is `element_hash` and version is `element_version` exists in the
# accumulator whose root hash is `expected_root_hash` using the provided proof.
def verify_accumulator_element(
        hash_func,
        expected_root_hash,
        element_hash,
        element_index,
        accumulator_proof):
    siblings = AccumulatorProof.from_proto(accumulator_proof).siblings
    assert len(siblings) <= MAX_ACCUMULATOR_PROOF_DEPTH
    index = element_index
    hashv = element_hash
    for sibling_hash in reversed(siblings):
        hasher = hash_func()
        if index % 2 == 0:
            hashv = MerkleTreeInternalNode(hashv, sibling_hash, hasher).hash()
        else:
            hashv = MerkleTreeInternalNode(sibling_hash, hashv, hasher).hash()
        index //= 2
    assert hashv == bytes(expected_root_hash)


# If `element_blob` is present, verifies an element whose key is `element_key` and value
# is `element_blob` exists in the Sparse Merkle Tree using the provided proof.
# Otherwise verifies the proof is a valid non-inclusion proof that shows this key doesn't exist
# in the tree.

def verify_sparse_merkle_element(
        expected_root_hash,
        element_key,
        element_blob,
        sparse_merkle_proof):
    proof = SparseMerkleProof.from_proto(sparse_merkle_proof)
    siblings = proof.siblings
    assert len(siblings) <= HashValue.LENGTH_IN_BITS
    if proof.leaf is not None:
        proof_key, proof_value_hash = proof.leaf
        if len(element_blob.__str__()) > 0:
            # This is an inclusion proof, so the key and value hash provided in the proof should
            # match element_key and element_value_hash.
            # `siblings` should prove the route from the leaf node to the root.
            ensure(
                element_key == proof_key,
                "Keys do not match. Key in proof: {}. Expected key: {}.",
                proof_key,
                element_key
            )
            hashv = AccountStateBlob.from_proto(element_blob).hash()
            ensure(
                hashv == proof_value_hash,
                "Value hashes do not match. Value hash in proof: {}. Expected value hash: {}",
                proof_value_hash,
                hashv
            )
        else:
            # This is a non-inclusion proof.
            # The proof intends to show that if a leaf node representing `element_key` is inserted,
            # it will break a currently existing leaf node represented by `proof_key` into a
            # branch.
            # `siblings` should prove the route from that leaf node to the root.
            ensure(
                element_key != proof_key,
                "Expected non-inclusion proof, but key exists in proof."
            )
            ensure(
                common_prefix_bits_len(element_key, proof_key) >= len(siblings),
                "Key would not have ended up in the subtree where the provided key in proof is \
                 the only existing key, if it existed. So this is not a valid non-inclusion proof."
            )
    else:
        if len(element_blob.__str__()) > 0:
            raise VerifyError("Expected inclusion proof. Found non-inclusion proof.")
        else:
            # This is a non-inclusion proof.
            # The proof intends to show that if a leaf node representing `element_key` is inserted,
            # it will show up at a currently empty position.
            # `sibling` should prove the route from this empty position to the root.
            pass
    if proof.leaf:
        key, value_hash = proof.leaf
        current_hash = SparseMerkleLeafNode(key, value_hash).hash()
    else:
        current_hash = bytes(SPARSE_MERKLE_PLACEHOLDER_HASH)
    iter_bits = bytes_to_bits(element_key)[0:len(siblings)]
    zipped = zip(reversed(siblings), reversed(iter_bits))
    for sibling_hash, bit in zipped:
        hasher = SparseMerkleInternalHasher()
        if bit == '1':
            current_hash = MerkleTreeInternalNode(sibling_hash, current_hash, hasher).hash()
        else:
            current_hash = MerkleTreeInternalNode(current_hash, sibling_hash, hasher).hash()
    ensure(
        current_hash == bytes(expected_root_hash),
        "Root hashes do not match. Actual root hash: {}. Expected root hash: {}.",
        current_hash,
        bytes(expected_root_hash)
    )


def verify_transaction_list(txn_list_with_proof, ledger_info):
    #TODO:change repeated SignedTransaction transactions = 1; to repeated Transaction transactions = 1;
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
    check_txn_list_sig_with_infos(txn_list_with_proof)
    #Get the hashes of all nodes at the accumulator leaf level.
    hashes = [TransactionInfo.from_proto(x).hash() for x in infos]
    hashes = collections.deque(hashes)
    firstp = AccumulatorProof.from_proto(txn_list_with_proof.proof_of_first_transaction)
    first = firstp.siblings
    if txn_list_with_proof.HasField("proof_of_last_transaction"):
        lastp = AccumulatorProof.from_proto(txn_list_with_proof.proof_of_last_transaction)
        last = lastp.siblings
    else:
        last = first
    first_idx = txn_list_with_proof.first_transaction_version.value
    zipped = zip(first, last)
    ite = reversed(list(zipped))
    for first_sibling, last_sibling in ite:
        num_nodes = len(hashes)
        if num_nodes > 1:
            last_idx = first_idx + num_nodes - 1
            if last_idx % 2 == 0:
                hashes.append(last_sibling)
            else:
                assert hashes[num_nodes - 2] == last_sibling
            if first_idx % 2 == 0:
                assert hashes[1] == first_sibling
            else:
                hashes.appendleft(first_sibling)
        else:
            assert first_sibling == last_sibling
            if first_idx % 2 == 0:
                hashes.append(first_sibling)
            else:
                hashes.appendleft(first_sibling)
        parent_hashes = collections.deque()
        for pair in more_itertools.chunked(hashes, 2):
            assert len(pair) == 2
            hasher = TransactionAccumulatorHasher()
            hash_value = MerkleTreeInternalNode(pair[0], pair[1], hasher).hash()
            parent_hashes.append(hash_value)
        hashes = parent_hashes
        first_idx //= 2
    assert len(hashes) == 1
    assert hashes[0] == bytes(ledger_info.transaction_accumulator_hash)




def check_txn_list_sig_with_infos(txn_list_with_proof):
    zipped = zip(txn_list_with_proof.transactions, txn_list_with_proof.infos)
    for tx, info in zipped:
        stx = SignedTransaction.from_proto(tx)
        if stx.hash() != info.signed_transaction_hash:
            raise VerifyError(f"transaction hash mismatch:{stx}.")

#Verify event root hashes match what is carried on the transaction infos.
def verify_event_root_hash(event_lists, infos):
    len_event = len(event_lists)
    len_info = len(infos)
    if len_info != len_event:
        raise VerifyError(f"transactions and events mismatch:{len_info}, {len_event}.")
    zipped = zip(event_lists, infos)
    for events, info in zipped:
        eroot_hash = get_event_root_hash(events.events)
        if bytes(eroot_hash) != info.event_root_hash:
            raise VerifyError(f"event_root_hash mismatch.")

