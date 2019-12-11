from canoser import Struct
from libra.account_config import AccountConfig
from libra.event import EventKey

class DiscoverySet(Struct):
    _fields = []

    DISCOVERY_SET_STRUCT_NAME = "DiscoverySet"

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.discovery_set_address(), 2)