from canoser import Struct, Uint64, Uint8
from libra.hasher import HashValue
from libra.account_address import Address
from libra.transaction.transaction_argument import ED25519_SIGNATURE_LENGTH


class BlockMetadata(Struct):
    _fields = [
        ('id', HashValue),
        ('timestamp_usec', Uint64),
        #('previous_block_votes', {Address, [Uint8, ED25519_SIGNATURE_LENGTH]}),
        ('previous_block_votes', {}),
        ('proposer', Address)
    ]

