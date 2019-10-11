from canoser import Struct, Uint8
from libra.transaction.transaction_argument import TransactionArgument


class Script(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument])
    ]