from canoser import Struct, Uint8, bytes_to_int_list, hex_to_int_list
from libra.transaction.transaction_argument import TransactionArgument
from libra.bytecode import bytecodes
from libra.account_address import Address


class Script(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument])
    ]

    @classmethod
    def gen_transfer_script(cls, receiver_address,micro_libra):
        if isinstance(receiver_address, bytes):
            receiver_address = bytes_to_int_list(receiver_address)
        if isinstance(receiver_address, str):
            receiver_address = hex_to_int_list(receiver_address)
        code = bytecodes["peer_to_peer_transfer"]
        args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U64', micro_libra)
            ]
        return Script(code, args)

    @classmethod
    def gen_mint_script(cls, receiver_address,micro_libra):
        receiver_address = Address.normalize_to_int_list(receiver_address)
        code = bytecodes["mint"]
        args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U64', micro_libra)
            ]
        return Script(code, args)

    @staticmethod
    def get_script_bytecode(script_name):
        return bytecodes[script_name]