from canoser import Struct
from canoser.types import *

class AccountState(Struct):
    _fields = [
        ('blob', {})
    ]

EVENT_KEY_LENGTH = 32

class EventHandle(Struct):
    _fields = [
        ('count', Uint64),
        #('key', [Uint8, EVENT_KEY_LENGTH])
        ('key', [Uint8])
    ]

class AccountResource(Struct):
    _fields = [
        ('authentication_key', [Uint8]),
        ('balance', Uint64),
        ('delegated_key_rotation_capability', bool),
        ('delegated_withdrawal_capability', bool),
        ('received_events', EventHandle),
        ('sent_events', EventHandle),
        ('sequence_number', Uint64)
    ]
