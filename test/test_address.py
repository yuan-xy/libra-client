from canoser import bytes_to_int_list
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

def test_equal_address():
    hexaddr = AccountConfig.association_address()
    bytesaddr = parse_address("0xa550c18")
    intsaddr = bytes_to_int_list(bytesaddr)
    assert Address.equal_address(hexaddr, bytesaddr)
    assert Address.equal_address(hexaddr, intsaddr)
    assert False == Address.equal_address(hexaddr, [])

def test_normalize_to_bytes():
    addr1 = Address.normalize_to_bytes([0]*ADDRESS_LENGTH)
    addr2 = parse_address("0"*HEX_ADDRESS_LENGTH)
    assert addr1 == addr2
