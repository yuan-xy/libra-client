from canoser import DelegateT, Struct, Uint64, Uint8


EVENT_KEY_LENGTH = 40

class EventKey(DelegateT):
    delegate_type = [Uint8, EVENT_KEY_LENGTH]


class EventHandle(Struct):
    _fields = [
        ('count', Uint64),#Number of events in the event stream.
        ('key', EventKey) #The associated globally unique key that is used as the key to the EventStore.
    ]

