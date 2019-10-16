from canoser import Struct, Uint64, bytes_to_int_list, hex_to_int_list
from datetime import datetime
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
    def new_write_set_tx(cls, sender_address, sequence_number, write_set):
        return RawTransaction(
            sender_address, sequence_number,
            TransactionPayload('WriteSet', write_set),
            # Since write-set transactions bypass the VM, these fields aren't relevant.
            0, 0,
            # Write-set transactions are special and important and shouldn't expire.
            Uint64.max_value
        )

    @classmethod
    def new_script_tx(cls, sender_address, sequence_number, script, max_gas_amount=140_000,
            gas_unit_price=0, txn_expiration=100):
        payload = TransactionPayload('Script', script)
        return cls.new_tx(sender_address, sequence_number, payload, max_gas_amount,
            gas_unit_price, txn_expiration)


    @classmethod
    def new_tx(cls, sender_address, sequence_number, payload, max_gas_amount=140_000,
            gas_unit_price=0, txn_expiration=100):
        sender_address = Address.normalize_to_int_list(sender_address)
        return RawTransaction(
            sender_address,
            sequence_number,
            payload,
            max_gas_amount,
            gas_unit_price,
            int(datetime.now().timestamp()) + txn_expiration
        )

    @classmethod
    def _gen_transfer_transaction(cls, sender_address, sequence_number, receiver_address,
        micro_libra, max_gas_amount=140_000, gas_unit_price=0, txn_expiration=100):
        script = Script.gen_transfer_script(receiver_address,micro_libra)
        return RawTransaction.new_script_tx(
            sender_address,
            sequence_number,
            script,
            max_gas_amount,
            gas_unit_price,
            txn_expiration
        )