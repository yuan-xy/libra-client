from libra.hasher import (
    HashValue, ACCUMULATOR_PLACEHOLDER_HASH,SPARSE_MERKLE_PLACEHOLDER_HASH,
    bytes_to_bits)
from libra.validator_verifier import VerifyError

# Because leaves can only take half the space in the tree, any numbering of the tree leaves must
# not take the full width of the total space.  Thus, for a 64-bit ordering, our maximumm proof
# depth is limited to 63.

#pub type LeafCount = u64;
MAX_ACCUMULATOR_PROOF_DEPTH = 63
MAX_ACCUMULATOR_LEAVES = 1 << MAX_ACCUMULATOR_PROOF_DEPTH

class AccumulatorProof:
    # All siblings in this proof, including the default ones. Siblings near the root are at the
    # beginning of the vector.
    def __init__(self, siblings):
        # The sibling list could be empty in case the accumulator is empty or has a single
        # element. When it's not empty, the top most sibling will never be default, otherwise the
        # accumulator should have collapsed to a smaller one.
        if len(siblings) > 0:
            assert siblings[0] != bytes(ACCUMULATOR_PLACEHOLDER_HASH)
        self.siblings = siblings

    @classmethod
    def from_proto(cls, proto_proof):
        bitmap = proto_proof.bitmap
        binstr = format(bitmap, 'b')
        num_non_default_siblings = binstr.count('1')
        assert num_non_default_siblings == len(proto_proof.non_default_siblings)
        # Iterate from the leftmost 1-bit to LSB in the bitmap. If a bit is set, the corresponding
        # sibling is non-default and we take the sibling from proto_siblings.  Otherwise the
        # sibling on this position is default.
        siblings = []
        index = 0
        for bit in binstr.lstrip('0'):
            if bit == '1':
                siblings.append(proto_proof.non_default_siblings[index])
                index += 1
            elif bit == '0':
                siblings.append(bytes(ACCUMULATOR_PLACEHOLDER_HASH))
            else:
                assert False
        return cls(siblings)


# A proof that can be used to authenticate an element in a Sparse Merkle Tree given trusted root
# hash. For example, `TransactionInfoToAccountProof` can be constructed on top of this structure.
class SparseMerkleProof:
    # This proof can be used to authenticate whether a given leaf exists in the tree or not.
    #     - If this is `Some(HashValue, HashValue)`
    #         - If the first `HashValue` equals requested key, this is an inclusion proof and the
    #           second `HashValue` equals the hash of the corresponding account blob.
    #         - Otherwise this is a non-inclusion proof. The first `HashValue` is the only key
    #           that exists in the subtree and the second `HashValue` equals the hash of the
    #           corresponding account blob.
    #     - If this is `None`, this is also a non-inclusion proof which indicates the subtree is
    #       empty.
    #leaf: Option<(HashValue, HashValue)>,

    # All siblings in this proof, including the default ones. Siblings near the root are at the
    # beginning of the vector.
    #siblings: Vec<HashValue>,

    def __init__(self, leaf, siblings):
        self.leaf = leaf
        # The sibling list could be empty in case the Sparse Merkle Tree is empty or has a single
        # element. When it's not empty, the bottom most sibling will never be default, otherwise a
        # leaf and a default sibling should have collapsed to a leaf.
        if len(siblings) > 0:
            assert siblings[-1] != bytes(SPARSE_MERKLE_PLACEHOLDER_HASH)
        self.siblings = siblings

    @classmethod
    def from_proto(cls, proto_proof):
        proto_leaf = proto_proof.leaf
        if proto_leaf:
            if len(proto_leaf) == HashValue.LENGTH * 2:
                key = proto_leaf[0:HashValue.LENGTH]
                value_hash = proto_leaf[HashValue.LENGTH:HashValue.LENGTH*2]
                leaf = (key, value_hash)
            else:
                raise VerifyError(f"Mailformed proof. Leaf has {len(proto_leaf)} bytes")
        else:
            leaf = None
        bitmap = proto_proof.bitmap
        if bitmap[-1] == b'0':
            raise VerifyError("Malformed proof. The last byte of the bitmap is zero.")
        bit_str = bytes_to_bits(bitmap)
        num_non_default_siblings = bit_str.count('1')
        if num_non_default_siblings != len(proto_proof.non_default_siblings):
            raise VerifyError("Malformed proof. Bitmap not match non-default siblings")
        proto_siblings = proto_proof.non_default_siblings
        #  Iterate from the MSB of the first byte to the rightmost 1-bit in the bitmap. If a bit is
        #  set, the corresponding sibling is non-default and we take the sibling from
        #  proto_siblings. Otherwise the sibling on this position is default.
        siblings = []
        index = 0
        for bit in bit_str.rstrip('0'):
            if bit == '1':
                siblings.append(proto_siblings[index])
                index += 1
            elif bit == '0':
                siblings.append(bytes(SPARSE_MERKLE_PLACEHOLDER_HASH))
            else:
                assert False
        return cls(leaf, siblings)

