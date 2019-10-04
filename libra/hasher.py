from libra.key_factory import new_sha3_256
import canoser

LIBRA_HASH_SUFFIX = b"@@$$LIBRA$$@@";

class HashValue(canoser.Struct):
    LENGTH = 32
    LENGTH_IN_BITS = LENGTH * 8
    LENGTH_IN_NIBBLES = LENGTH * 2

    _fields = [
        ('hash', [canoser.Uint8, LENGTH])
    ]


def hash_seed(clazz):
    sha3 = new_sha3_256()
    sha3.update(clazz+LIBRA_HASH_SUFFIX)
    return sha3.digest()

def raw_tx_hash(raw_tx):
    raw_txn_bytes = raw_tx.serialize()
    salt = hash_seed(b"RawTransaction")
    shazer = new_sha3_256()
    shazer.update(salt)
    shazer.update(raw_txn_bytes)
    return shazer.digest()

def gen_hasher(name_in_bytes):
    salt = hash_seed(name_in_bytes)
    shazer = new_sha3_256()
    shazer.update(salt)
    return shazer

def EventAccumulatorHasher():
    return gen_hasher(b"EventAccumulator")


def create_literal_hash(word):
    arr = [ord(x) for x in list(word)]
    assert len(arr) <= HashValue.LENGTH
    for _i in range(len(arr), HashValue.LENGTH):
        arr.append(0)
    return HashValue(arr)

ACCUMULATOR_PLACEHOLDER_HASH = create_literal_hash("ACCUMULATOR_PLACEHOLDER_HASH")
SPARSE_MERKLE_PLACEHOLDER_HASH = create_literal_hash("SPARSE_MERKLE_PLACEHOLDER_HASH")
PRE_GENESIS_BLOCK_ID = create_literal_hash("PRE_GENESIS_BLOCK_ID")
GENESIS_BLOCK_ID = create_literal_hash("GENESIS_BLOCK_ID")
