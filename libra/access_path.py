from canoser import Struct, Uint8, Uint64, RustEnum, DelegateT, bytes_to_int_list, hex_to_int_list
from libra.account_address import Address
from libra.account_config import AccountConfig
from libra.language_storage import ModuleId
from typing import List

#SEPARATOR is used as a delimiter between fields. It should not be a legal part of any identifier
#in the language
SEPARATOR = '/'

class Field(DelegateT):
    delegate_type = str #Identifier


class Access(RustEnum):
    _enums = [
        ('Field', str),
        ('Index', Uint64)
    ]


class Accesses(DelegateT):
    delegate_type = [Access]

    @staticmethod
    def as_separated_string(obj: List[Access]) -> str:
        path = ""
        for access in obj:
            if access.Field:
                path += access.value
            elif access.Index:
                path += str(access.value)
            else:
                raise AssertionError("Unreachable")
            path += SEPARATOR
        return path


class AccessPath(Struct):
    _fields = [
        ('address', Address),
        ('path', [Uint8])
    ]

    CODE_TAG = 0
    RESOURCE_TAG = 1

    @staticmethod
    def str_to_ints(astr):
        return [x for x in str.encode(astr)]

    @classmethod
    def resource_access_vec(cls, tag, accesses):
        key = []
        key.append(cls.RESOURCE_TAG)
        key.extend(bytes_to_int_list(tag.hash()))
        #We don't need accesses in production right now. Accesses are appended here just for
        #passing the old tests.
        astr = Accesses.as_separated_string(accesses)
        key.extend(AccessPath.str_to_ints(astr))
        return key

    @classmethod
    def code_access_path_vec(cls, key: ModuleId):
        root = []
        root.append(cls.CODE_TAG)
        root.extend(bytes_to_int_list(key.hash()))
        return root

    @classmethod
    def code_access_path(cls, key: ModuleId):
        path = AccessPath.code_access_path_vec(key)
        return AccessPath(key.address, path)



# VALIDATOR_SET_ACCESS_PATH = AccessPath(
#     hex_to_int_list(AccountConfig.association_address()),
#     ValidatorSet.validator_set_path()
# )