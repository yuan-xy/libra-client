from canoser import *
from datetime import datetime
from nacl.signing import VerifyKey
from libra.bytecode import bytecode, get_transaction_name
from libra.account_address import Address
from libra.hasher import gen_hasher, HashValue
from libra.access_path import AccessPath

# must define type by serialized sequence, not the sequence in the rust struct definition.
# ack 'impl CanonicalSerialize for {type}' -A 20

ED25519_PUBLIC_KEY_LENGTH = 32
ED25519_SIGNATURE_LENGTH = 64

class TransactionArgument(RustEnum):
    _enums = [
        ('U64', Uint64),
        ('Address', Address),
        ('String', str),
        ('ByteArray', [Uint8])
    ]

class WriteOp(RustEnum):
    _enums = [
        ('Deletion', None),
        ('Value', [Uint8])
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

    @classmethod
    def pretty_print_field(cls, field_name, field_type, field_value, buffer, ident):
        if field_name == 'code':
            transaction_name = get_transaction_name(field_value)
            buffer.write(f'{field_name}: <{transaction_name}>')
        else:
            super().pretty_print_field(field_name, field_type, field_value, buffer, ident)

class TransactionPayload(RustEnum):
    _enums = [
        ('Program', Program),
        ('WriteSet', WriteSet),
        ('Script', Script),
        ('Module', Module)
    ]

class RawTransaction(Struct):
    _fields = [
        ('sender', Address),
        ('sequence_number', Uint64),
        ('payload', TransactionPayload),
        ('max_gas_amount', Uint64),
        ('gas_unit_price', Uint64),
        ('expiration_time', Uint64)
    ]

    def hash(self):
        shazer = gen_hasher(b"RawTransaction")
        shazer.update(self.serialize())
        return shazer.digest()

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
            int(datetime.now().timestamp()) + txn_expiration
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
    def gen_from_raw_txn(cls, raw_tx, sender_account):
        tx_hash = raw_tx.hash()
        signature = sender_account.sign(tx_hash)[:64]
        return SignedTransaction(raw_tx,
                bytes_to_int_list(sender_account.public_key),
                bytes_to_int_list(signature)
            )

    def hash(self):
        shazer = gen_hasher(b"SignedTransaction")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        return cls.deserialize(proto.signed_txn)

    def check_signature(self):
        message = self.raw_txn.hash()
        vkey = VerifyKey(bytes(self.public_key))
        vkey.verify(message, bytes(self.signature))

    @property
    def sender(self):
        return self.raw_txn.sender

    @property
    def sequence_number(self):
        return self.raw_txn.sequence_number

    @property
    def payload(self):
        return self.raw_txn.payload

    @property
    def max_gas_amount(self):
        return self.raw_txn.max_gas_amount

    @property
    def gas_unit_price(self):
        return self.raw_txn.gas_unit_price

    @property
    def expiration_time(self):
        return self.raw_txn.expiration_time


class TransactionInfo(Struct):
    _fields = [
        ('signed_transaction_hash', HashValue),
        ('state_root_hash', HashValue),
        ('event_root_hash', HashValue),
        ('gas_used', Uint64),
        ('major_status', Uint64)
    ]

    def hash(self):
        shazer = gen_hasher(b"TransactionInfo")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        ret = cls()
        ret.signed_transaction_hash = bytes_to_int_list(proto.signed_transaction_hash)
        ret.state_root_hash = bytes_to_int_list(proto.state_root_hash)
        ret.event_root_hash = bytes_to_int_list(proto.event_root_hash)
        ret.gas_used = proto.gas_used
        ret.major_status = proto.major_status
        return ret
