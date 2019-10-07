from libra.key_factory import new_sha3_256
import canoser

LIBRA_HASH_SUFFIX = b"@@$$LIBRA$$@@";

class HashValue(canoser.DelegateT):
    LENGTH = 32
    LENGTH_IN_BITS = LENGTH * 8
    LENGTH_IN_NIBBLES = LENGTH * 2
    delegate_type = [canoser.Uint8, LENGTH]

def uint8_to_bits(uint8):
    return format(uint8, '8b').replace(' ', '0')

def bytes_to_bits(abytes):
    return ''.join([uint8_to_bits(x) for x in abytes])

def common_prefix_bits_len(bytes1, bytes2):
    assert len(bytes1) == len(bytes2)
    bit_str1 = ''.join([uint8_to_bits(x) for x in bytes1])
    bit_str2 = ''.join([uint8_to_bits(x) for x in bytes2])
    for idx, bit in enumerate(bit_str1):
        if bit != bit_str2[idx]:
            return idx
    return len(bit_str1)


def hash_seed(clazz_name):
    sha3 = new_sha3_256()
    sha3.update(clazz_name+LIBRA_HASH_SUFFIX)
    return sha3.digest()

def gen_hasher(name_in_bytes):
    salt = hash_seed(name_in_bytes)
    shazer = new_sha3_256()
    shazer.update(salt)
    return shazer

def EventAccumulatorHasher():
    return gen_hasher(b"EventAccumulator")

def TransactionAccumulatorHasher():
    return gen_hasher(b"TransactionAccumulator")

def SparseMerkleInternalHasher():
    return gen_hasher(b"SparseMerkleInternal")

def create_literal_hash(word):
    arr = [ord(x) for x in list(word)]
    assert len(arr) <= HashValue.LENGTH
    for _i in range(len(arr), HashValue.LENGTH):
        arr.append(0)
    return arr

ACCUMULATOR_PLACEHOLDER_HASH = create_literal_hash("ACCUMULATOR_PLACEHOLDER_HASH")
SPARSE_MERKLE_PLACEHOLDER_HASH = create_literal_hash("SPARSE_MERKLE_PLACEHOLDER_HASH")
PRE_GENESIS_BLOCK_ID = create_literal_hash("PRE_GENESIS_BLOCK_ID")
GENESIS_BLOCK_ID = create_literal_hash("GENESIS_BLOCK_ID")
