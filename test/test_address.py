from libra.account_address import *
from libra.account_config import AccountConfig

def test_parse():
    address = bytes.fromhex("000000000000000000000000000000000000000000000000000000000a550c18")
    assert parse_address(AccountConfig.association_address()) == address
    assert parse_address("0xa550c18") == address
    assert parse_address("0xA550c18") == address
    assert parse_address("0x0A550c18") == address
    assert parse_address("a550c18") is None
    assert parse_address(AccountConfig.association_address()+"1") is None
