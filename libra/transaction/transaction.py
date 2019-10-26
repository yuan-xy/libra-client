from canoser import RustEnum
from libra.transaction.signed_transaction import SignedTransaction
from libra.transaction.write_set import WriteSet
from libra.block_metadata import BlockMetadata


class Transaction(RustEnum):
    _enums = [
        ('UserTransaction', SignedTransaction),
        ('WriteSet', WriteSet),
        ('BlockMetadata', BlockMetadata)
    ]
