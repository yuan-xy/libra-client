from canoser import DelegateT, Struct, Uint64, Uint8, bytes_to_int_list
from libra.account_address import Address


EVENT_KEY_LENGTH = 40

class EventKey(DelegateT):
    delegate_type = [Uint8, EVENT_KEY_LENGTH]

    @classmethod
    def new_from_address(cls, addr, salt):
        lhs = Uint64.encode(salt)
        rhs = Address.normalize_to_bytes(addr)
        output_bytes = lhs + rhs
        return bytes_to_int_list(output_bytes)



class EventHandle(Struct):
    _fields = [
        ('count', Uint64),#Number of events in the event stream.
        ('key', EventKey) #The associated globally unique key that is used as the key to the EventStore.
    ]

