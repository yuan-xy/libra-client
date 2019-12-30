from canoser import DelegateT
from libra.account_config import AccountConfig
from libra.event import EventKey
from libra.discovery_info import DiscoveryInfo

class DiscoverySet(DelegateT):
    delegate_type = [DiscoveryInfo]

    DISCOVERY_SET_STRUCT_NAME = "DiscoverySet"

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.discovery_set_address(), 2)