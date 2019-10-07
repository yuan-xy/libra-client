from libra.hasher import ACCUMULATOR_PLACEHOLDER_HASH

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
        for bit in binstr:
            if bit == '1':
                siblings.append(proto_proof.non_default_siblings[index])
                index += 1
            elif bit == '0':
                siblings.append(bytes(ACCUMULATOR_PLACEHOLDER_HASH))
            else:
                assert False
        return cls(siblings)

