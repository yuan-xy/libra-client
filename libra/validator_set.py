from canoser import DelegateT, hex_to_int_list
from libra.validator_public_keys import ValidatorPublicKeys
from libra.account_config import AccountConfig
from libra.account_address import Address
from libra.language_storage import StructTag
from libra.access_path import AccessPath
from libra.event import EventKey

class ValidatorSet(DelegateT):
    delegate_type = [ValidatorPublicKeys]

    LIBRA_SYSTEM_MODULE_NAME = "LibraSystem"
    VALIDATOR_SET_STRUCT_NAME = "ValidatorSet"


    VALIDATOR_SET_MODULE_NAME = LIBRA_SYSTEM_MODULE_NAME

    @classmethod
    def validator_set_tag(cls) -> StructTag:
        return StructTag(
            hex_to_int_list(AccountConfig.core_code_address()),
            cls.VALIDATOR_SET_MODULE_NAME,
            cls.VALIDATOR_SET_STRUCT_NAME,
            []
        )

    @classmethod
    def validator_set_path(cls):
        return AccessPath.resource_access_vec(cls.validator_set_tag(), [])

    @classmethod
    def change_event_key(cls):
        return EventKey.new_from_address(AccountConfig.validator_set_address(), 2)

    @classmethod
    def from_proto(cls, next_validator_set_proto):
        ret = []
        for keys in next_validator_set_proto.validator_public_keys:
            ret.append(ValidatorPublicKeys.from_proto(keys))
        return ret
