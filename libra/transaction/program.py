from canoser import Struct, Uint8
from libra.transaction.transaction_argument import TransactionArgument


class Program(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument]),
        ('modules', [[Uint8]])
    ]
