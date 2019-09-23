from canoser import *
from canoser.types import *
from datetime import datetime
from libra.bytecode import bytecode

# must define type by serialized sequence, not the sequence in the rust struct definition.
# ack 'impl CanonicalSerialize for {type}' -A 20

ADDRESS_LENGTH = 32
ED25519_PUBLIC_KEY_LENGTH = 32
ED25519_SIGNATURE_LENGTH = 64


#pub struct ByteArray(Vec<u8>);

class TransactionArgument(RustEnum):
    _enums = [
        ('U64', Uint64),
        ('Address', [Uint8, ADDRESS_LENGTH]),
        ('String', str),
        ('ByteArray', [Uint8])
    ]

class WriteOp(RustEnum):
    _enums = [
        ('Deletion', None),
        ('Value', [Uint8])
    ]

class AccessPath(Struct):
    _fields = [
        ('address', [Uint8, ADDRESS_LENGTH]),
        ('path', [Uint8])
    ]


class Program(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument]),
        ('modules', [[Uint8]])
    ]


# `WriteSet` contains all access paths that one transaction modifies. Each of them is a `WriteOp`
# where `Value(val)` means that serialized representation should be updated to `val`, and
# `Deletion` means that we are going to delete this access path.
class WriteSet(Struct):
    _fields = [
        ('write_set', [(AccessPath, WriteOp)])
    ]


class Module(Struct):
    _fields = [
        ('code', [Uint8])
    ]


class Script(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument])
    ]

class TransactionPayload(RustEnum):
    _enums = [
        ('Program', Program),
        ('WriteSet', WriteSet),
        ('Script', Script),
        ('Module', Module)
    ]

class RawTransaction(Struct):
    _fields = [
        ('sender', [Uint8, ADDRESS_LENGTH]),
        ('sequence_number', Uint64),
        ('payload', TransactionPayload),
        ('max_gas_amount', Uint64),
        ('gas_unit_price', Uint64),
        ('expiration_time', Uint64)
    ]

    @classmethod
    def new_write_set(cls, sender_address, sequence_number, write_set):
        return RawTransaction(
            sender_address, sequence_number,
            TransactionPayload('WriteSet', write_set),
            # Since write-set transactions bypass the VM, these fields aren't relevant.
            0, 0,
            # Write-set transactions are special and important and shouldn't expire.
            Uint64.max_value
        )

    @classmethod
    def gen_transfer_transaction(cls, sender_address, sequence_number, receiver_address,
        micro_libra, max_gas_amount=140_000, gas_unit_price=0, txn_expiration=100):
        if isinstance(sender_address, bytes):
            sender_address = bytes_to_int_list(sender_address)
        if isinstance(sender_address, str):
            sender_address = hex_to_int_list(sender_address)
        if isinstance(receiver_address, bytes):
            receiver_address = bytes_to_int_list(receiver_address)
        if isinstance(receiver_address, str):
            receiver_address = hex_to_int_list(receiver_address)
        code = cls.get_script_bytecode("peer_to_peer_transfer")
        script = Script(
            code,
            [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U64', micro_libra)
            ]
        )
        return RawTransaction(
            sender_address,
            sequence_number,
            TransactionPayload('Script', script),
            max_gas_amount,
            gas_unit_price,
            int(datetime.utcnow().timestamp()) + txn_expiration
        )


    @classmethod
    def gen_mint_transaction(cls, receiver, micro_libra):
        pass
        #TODO:

    @staticmethod
    def get_script_bytecode(script_name):
        return bytecode[script_name]

    @staticmethod
    def get_script_bytecode_deprecated(script_file):
        with open(script_file) as f:
            data = f.read()
            amap = eval(data)
            return amap['code']


class SignedTransaction(Struct):
    _fields = [
        ('raw_txn', RawTransaction),
        ('public_key', [Uint8, ED25519_PUBLIC_KEY_LENGTH]),
        ('signature', [Uint8, ED25519_SIGNATURE_LENGTH])
#        ('transaction_length', Uint64)
    ]

    @classmethod
    def new_for_bytes_key(cls, raw_tx, public_key, signature):
        return SignedTransaction(raw_tx,
                bytes_to_int_list(public_key),
                bytes_to_int_list(signature)
            )



def int_list_to_hex(ints):
    return struct.pack("<{}B".format(len(ints)), *ints).hex()

def bytes_to_int_list(bytes_str):
    tp = struct.unpack("<{}B".format(len(bytes_str)), bytes_str)
    return list(tp)

def hex_to_int_list(hex_str):
    return bytes_to_int_list(bytes.fromhex(hex_str))