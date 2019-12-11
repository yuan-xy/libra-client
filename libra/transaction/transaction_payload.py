from canoser import RustEnum
from libra.transaction.change_set import ChangeSet
from libra.transaction.script import Script
from libra.transaction.module import Module


class TransactionPayload(RustEnum):
    _enums = [
        ('Program', None),
        ('WriteSet', ChangeSet),
        ('Script', Script),
        ('Module', Module)
    ]
