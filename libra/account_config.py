from canoser import hex_to_int_list, Struct, Uint64
from libra.language_storage import StructTag
from libra.account_address import HEX_ADDRESS_LENGTH, Address

class AccountConfig:
    # LibraCoin
    COIN_MODULE_NAME = "LibraCoin";
    COIN_STRUCT_NAME = "T";

    # Account
    ACCOUNT_MODULE_NAME = "LibraAccount";
    ACCOUNT_STRUCT_NAME = "T";

    # Hash
    HASH_MODULE_NAME = "Hash";


    @classmethod
    def account_resource_path(cls):
        #return AccessPath.resource_access_vec(AccountConfig.account_struct_tag(), [])
        return b'\x01\xa2\x08\xdf\x13O\xef\xed\x84B\xb1\xf0\x1f\xabY\x07\x18\x98\xf5\xa1\xafQd\xe1,YM\xe5Zp\x04\xa9\x1c'

    @classmethod
    def account_sent_event_path(cls):
        return cls.account_resource_path() + b"/sent_events_count/"

    @classmethod
    def account_received_event_path(cls):
        return cls.account_resource_path() + b"/received_events_count/"

    @classmethod
    def core_code_address(cls):
        return "0".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def core_code_address_ints(cls):
        return Address.normalize_to_int_list(cls.core_code_address())

    @classmethod
    def association_address(cls):
        return "a550c18".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def association_address_ints(cls):
        return Address.normalize_to_int_list(cls.association_address())

    @classmethod
    def transaction_fee_address(cls):
        return "FEE".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def validator_set_address(cls):
        return "1d8".rjust(HEX_ADDRESS_LENGTH, '0')

    @classmethod
    def account_struct_tag(cls):
        return StructTag(
            hex_to_int_list(cls.core_code_address()),
            cls.ACCOUNT_MODULE_NAME,
            cls.ACCOUNT_STRUCT_NAME,
            []
        )

    @classmethod
    def all_config(cls):
        return {
            "core_code_address" : AccountConfig.core_code_address(),
            "association_address" : AccountConfig.association_address(),
            "validator_set_address" : AccountConfig.validator_set_address(),
            "account_resource_path": AccountConfig.account_resource_path(),
            "account_sent_event_path" : AccountConfig.account_sent_event_path(),
            "account_received_event_path" : AccountConfig.account_received_event_path()
        }


class AccountEvent(Struct):
    _fields = [
        ('amount', Uint64),
        ('account', Address)
    ]

