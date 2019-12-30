from canoser import RustEnum, Uint64, Uint8, bytes_to_int_list, hex_to_int_list
from libra.account_address import Address, parse_address
from libra.crypto.ed25519 import ED25519_PUBLIC_KEY_LENGTH, ED25519_SIGNATURE_LENGTH

def normalize_public_key(public_key):
    if isinstance(public_key, list):
        if len(public_key) != ED25519_PUBLIC_KEY_LENGTH:
            raise ValueError(f"{public_key} is not a valid public_key.")
        return public_key
    if isinstance(public_key, bytes):
        if len(public_key) != ED25519_PUBLIC_KEY_LENGTH:
            raise ValueError(f"{public_key} is not a valid public_key.")
        return bytes_to_int_list(public_key)
    if isinstance(public_key, str):
        if len(public_key) != ED25519_PUBLIC_KEY_LENGTH*2:
            raise ValueError(f"{public_key} is not a valid public_key.")
        return hex_to_int_list(public_key)


class TransactionArgument(RustEnum):
    _enums = [
        ('U64', Uint64),
        ('Address', Address),
        ('ByteArray', [Uint8]),
        ('Bool', bool)
    ]

    @classmethod
    #Parses the given string as any transaction argument type.
    def parse_as_transaction_argument(cls, s):
        address = parse_address(s)
        if address is not None:
            return TransactionArgument('Address', bytes_to_int_list(address))
        elif s[0:2] == 'b"' and s[-1] == '"' and len(s) > 3:
            barr = bytes.fromhex(s[2:-1])
            return TransactionArgument('ByteArray', bytes_to_int_list(barr))
        else:
            try:
                i = Uint64.int_safe(s)
                return TransactionArgument('U64', i)
            except Exception:
                raise
        raise TypeError(f"cannot parse {s} as transaction argument")
        #TODO: why not support String type.

