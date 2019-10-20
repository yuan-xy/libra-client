from libra.hasher import *
from libra.event import ContractEvent
import more_itertools


class MerkleTreeInternalNode:
    def __init__(self, left_child, right_child, hasher):
        self.left_child = left_child
        self.right_child = right_child
        self.hasher = hasher

    def hash(self):
        self.hasher.update(self.left_child)
        self.hasher.update(self.right_child)
        return self.hasher.digest()


def get_accumulator_root_hash(hasher, element_hashes):
    def compute_tree_hash(t):
        if len(t) == 2:
            return MerkleTreeInternalNode(t[0], t[1], hasher).hash()
        else:
            import pdb
            pdb.set_trace()
            #TODO: how to test this branch
            return MerkleTreeInternalNode(t[0], ACCUMULATOR_PLACEHOLDER_HASH, hasher).hash()
    if not element_hashes:
        return ACCUMULATOR_PLACEHOLDER_HASH
    next_level = []
    current_level = element_hashes
    while len(current_level) > 1:
        next_level = [compute_tree_hash(x) for x in more_itertools.chunked(current_level, 2)]
        current_level = next_level
    return current_level[0]

def get_event_root_hash(events):
    event_hashes = [ContractEvent.from_proto(x).hash() for x in events]
    return get_accumulator_root_hash(EventAccumulatorHasher(), event_hashes)


class SparseMerkleLeafNode:
    def __init__(self, key, value_hash):
        self.key = key
        self.value_hash = value_hash

    def hash(self):
        shazer = gen_hasher(b"SparseMerkleLeaf")
        shazer.update(self.key)
        shazer.update(self.value_hash)
        return shazer.digest()
