from libra.access_path import *
from libra.account_config import AccountConfig
from libra.language_storage import ModuleId
from canoser import hex_to_int_list

#import pdb

def test_resource_access_vec():
    array = AccessPath.resource_access_vec(AccountConfig.account_struct_tag(), [])
    assert bytes(array) == AccountConfig.account_resource_path()

def test_code_access_path():
    address = hex_to_int_list('795b209248c746de5fc1fc3bd7e1b41aee88916dd8ddfe29dd44fa75ce019dda')
    mid = ModuleId(address, 'Pay')
    assert mid.address == address
    assert mid.name == 'Pay'
    path = AccessPath.code_access_path_vec(mid)
    assert len(path) == 33
    assert path[0] == 0
    assert bytes(path).hex() == "009b4ca94864a2d83530b729a55fa4be6c3119eed470571793656a7cc36b5a7767"
    ap = AccessPath.code_access_path(mid)
    assert ap.address == address
    assert ap.path == path