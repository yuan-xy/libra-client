from canoser import Struct, Uint8, bytes_to_int_list, hex_to_int_list
from nacl.signing import VerifyKey
from libra.hasher import gen_hasher, HashValue
from libra.transaction.raw_transaction import RawTransaction
from libra.transaction.transaction_argument import ED25519_PUBLIC_KEY_LENGTH, ED25519_SIGNATURE_LENGTH


class SignedTransaction(Struct):
    _fields = [
        ('raw_txn', RawTransaction),
        ('public_key', [Uint8, ED25519_PUBLIC_KEY_LENGTH]),
        ('signature', [Uint8, ED25519_SIGNATURE_LENGTH])
#        ('transaction_length', Uint64)
    ]

    def check_events(self, event_list):
        if len(event_list.events) > 0:
            self.success = True
        else:
            self.success = False

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        if hasattr(self, 'success'):
            amap["success"] = self.success
        return amap

    @classmethod
    def gen_from_raw_txn(cls, raw_tx, sender_account):
        tx_hash = raw_tx.hash()
        signature = sender_account.sign(tx_hash)[:64]
        return SignedTransaction(raw_tx,
                bytes_to_int_list(sender_account.public_key),
                bytes_to_int_list(signature)
            )

    def hash(self):
        shazer = gen_hasher(b"SignedTransaction")
        shazer.update(self.serialize())
        return shazer.digest()

    @classmethod
    def from_proto(cls, proto):
        return cls.deserialize(proto.signed_txn)

    def check_signature(self):
        message = self.raw_txn.hash()
        vkey = VerifyKey(bytes(self.public_key))
        vkey.verify(message, bytes(self.signature))

    @property
    def sender(self):
        return self.raw_txn.sender

    @property
    def sequence_number(self):
        return self.raw_txn.sequence_number

    @property
    def payload(self):
        return self.raw_txn.payload

    @property
    def max_gas_amount(self):
        return self.raw_txn.max_gas_amount

    @property
    def gas_unit_price(self):
        return self.raw_txn.gas_unit_price

    @property
    def expiration_time(self):
        return self.raw_txn.expiration_time
