from libra.access_path import *
from libra.account_config import AccountConfig
import pdb

def test_resource_access_vec():
    array = AccessPath.resource_access_vec(AccountConfig.account_struct_tag(), [])
    assert bytes(array) == AccountConfig.account_resource_path()
