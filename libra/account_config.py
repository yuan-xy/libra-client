from canoser import hex_to_int_list
from libra.language_storage import StructTag
from libra.account_address import HEX_ADDRESS_LENGTH

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
        return bytes.fromhex("01217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc97")

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
    def association_address(cls):
        return "a550c18".rjust(HEX_ADDRESS_LENGTH, '0')

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