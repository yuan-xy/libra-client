from libra.proto.transaction_pb2 import RawTransaction
from libra.proto.transaction_pb2 import TransactionArgument
import libra
from datetime import datetime

PEER_TO_PEER_TXN = '4c49425241564d0a010007014a00000004000000034e000000060000000c54000000060000000d5a0000000600000005600000002900000004890000002000000007a90000000f00000000000001000200010300020002040200030003020402063c53454c463e0c4c696272614163636f756e74046d61696e0f7061795f66726f6d5f73656e6465720000000000000000000000000000000000000000000000000000000000000000000100020104000c000c0113010002'

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
        program.code = bytes.fromhex(self.opcodes)
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
        tran = cls(PEER_TO_PEER_TXN, ["address", "u64"], [receiver, value])
        return tran


