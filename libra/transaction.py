from libra.proto.transaction_pb2 import RawTransaction
from libra.proto.transaction_pb2 import TransactionArgument
import libra
from datetime import datetime

class Transaction:
    def to_raw_tx_proto(
        self, sender, sequence_number, max_gas_amount=140_000, gas_unit_price=0, txn_expiration=100
    ):
        raw_tx = RawTransaction()
        raw_tx.sender_account = sender.address
        raw_tx.sequence_number = sequence_number
        raw_tx.max_gas_amount = max_gas_amount
        raw_tx.gas_unit_price = gas_unit_price
        expiration_time = int(datetime.utcnow().timestamp()) + txn_expiration
        raw_tx.expiration_time = expiration_time
        self.fill_program(raw_tx.program)
        return raw_tx


    def __init__(self, opcodes, arg_types, arg_vals):
        self.opcodes = opcodes
        self.arg_types = arg_types
        self.arg_vals = arg_vals

    def fill_program(self, program):
        program.code = self.opcodes
        for kind, val in zip(self.arg_types, self.arg_vals):
            arg = program.arguments.add()
            if kind.lower() == "address":
                if isinstance(val, libra.Account):
                    val = val.address_hex
                arg.type = TransactionArgument.ADDRESS
                arg.data = bytes.fromhex(val)
            elif kind.lower() == "u64":
                arg.type = TransactionArgument.U64
                arg.data = val.to_bytes(8, "little")
            else:
                raise ValueError("Unknown arg type: {}".format(kind))

    @classmethod
    def gen_transfer_transaction(cls, receiver, value):
        code = get_script_bytecode("transaction_scripts/peer_to_peer_transfer.bytecode")
        tran = cls(code, ["address", "u64"], [receiver, value])
        return tran

    @staticmethod
    def get_script_bytecode(script_file):
        with open(script_file) as f:
            data = f.read()
            amap = eval(data)
            return bytes(amap['code'])


