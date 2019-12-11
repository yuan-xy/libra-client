from canoser import Struct, Uint64, Uint8
from libra.hasher import HashValue
from libra.account_address import Address
from libra.transaction.transaction_argument import ED25519_SIGNATURE_LENGTH


class BlockMetadata(Struct):
    _fields = [
        ('id', HashValue),
        ('timestamp_usec', Uint64),
        ('previous_block_votes', {Address: [Uint8, ED25519_SIGNATURE_LENGTH]}),
        ('proposer', Address)
    ]


    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'transaction_info'):
            amap["transaction_info"] = self.transaction_info.to_json_serializable()
        if hasattr(self, 'events'):
            amap["events"] = [x.to_json_serializable() for x in self.events]
        if hasattr(self, 'version'):
            amap["version"] = self.version
        if hasattr(self, 'success'):
            amap["success"] = self.success
        return amap