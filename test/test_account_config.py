from libra.account_config import *

def test_address():
    assert AccountConfig.association_address() == "000000000000000000000000000000000000000000000000000000000a550c18"
