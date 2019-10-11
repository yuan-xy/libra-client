from canoser import RustEnum, Uint64, Uint8, bytes_to_int_list
from libra.account_address import Address, parse_address


class TransactionArgument(RustEnum):
    _enums = [
        ('U64', Uint64),
        ('Address', Address),
        ('String', str),
        ('ByteArray', [Uint8])
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
                i = int(s)
                return TransactionArgument('U64', i)
            except Exception:
                raise
        raise TypeError(f"cannot parse {s} as transaction argument")
        #TODO: why not support String type.

