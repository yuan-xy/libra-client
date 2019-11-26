from canoser import RustEnum
from libra.transaction.program import Program
from libra.transaction.write_set import WriteSet
from libra.transaction.script import Script
from libra.transaction.module import Module


class TransactionPayload(RustEnum):
    _enums = [
        ('Program', None),
        ('WriteSet', WriteSet),
        ('Script', Script),
        ('Module', Module)
    ]
