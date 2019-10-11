from canoser import Struct, Uint64, bytes_to_int_list, hex_to_int_list
from datetime import datetime
from libra.bytecode import bytecode, get_transaction_name
from libra.account_address import Address
from libra.hasher import gen_hasher, HashValue
from libra.transaction.transaction_payload import TransactionPayload
from libra.transaction.transaction_argument import TransactionArgument
from libra.transaction.script import Script


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
    def new_script(cls, sender_address, sequence_number, script_code, script_args, max_gas_amount=140_000, gas_unit_price=0, txn_expiration=100):
        if isinstance(sender_address, bytes):
            sender_address = bytes_to_int_list(sender_address)
        if isinstance(sender_address, str):
            sender_address = hex_to_int_list(sender_address)
        return RawTransaction(
            sender_address,
            sequence_number,
            TransactionPayload('Script', Script(script_code, script_args)),
            max_gas_amount,
            gas_unit_price,
            int(datetime.now().timestamp()) + txn_expiration
        )

    @classmethod
    def gen_transfer_transaction(cls, sender_address, sequence_number, receiver_address,
        micro_libra, max_gas_amount=140_000, gas_unit_price=0, txn_expiration=100):
        if isinstance(receiver_address, bytes):
            receiver_address = bytes_to_int_list(receiver_address)
        if isinstance(receiver_address, str):
            receiver_address = hex_to_int_list(receiver_address)
        code = cls.get_script_bytecode("peer_to_peer_transfer")
        args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U64', micro_libra)
            ]
        return RawTransaction.new_script(
            sender_address,
            sequence_number,
            code,
            args,
            max_gas_amount,
            gas_unit_price,
            txn_expiration
        )


    @classmethod
    def gen_mint_transaction(cls, receiver, micro_libra):
        pass
        #TODO:

    @staticmethod
    def get_script_bytecode(script_name):
        return bytecode[script_name]

