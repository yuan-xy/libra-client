from canoser import bytes_to_int_list
from libra.account_address import *
from libra.account_config import AccountConfig
import pytest

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
    assert False == Address.equal_address(hexaddr, parse_address("0x123"))

def test_normalize_to_bytes():
    addr1 = Address.normalize_to_bytes([0]*ADDRESS_LENGTH)
    addr2 = parse_address("0"*HEX_ADDRESS_LENGTH)
    assert addr1 == addr2

def normalize_to_int_list():
    addr0 = [0]*ADDRESS_LENGTH
    addr1 = Address.normalize_to_int_list(addr0)
    assert addr0 == addr1
    addr2 = Address.normalize_to_int_list("0"*HEX_ADDRESS_LENGTH)
    assert addr1 == addr2
    addr3 = Address.normalize_to_int_list(parse_address("0"*HEX_ADDRESS_LENGTH))
    assert addr1 == addr3

def test_strict_parse_address():
    address = bytes.fromhex("000000000000000000000000000000000000000000000000000000000a550c18")
    hexstr = AccountConfig.association_address()
    assert strict_parse_address(hexstr) == address
    assert strict_parse_address("0x"+hexstr) == address
    assert strict_parse_address(f"'{hexstr}'") == address
    assert strict_parse_address(f'"{hexstr}"') == address
    with pytest.raises(ValueError):
        strict_parse_address("0"+hexstr)
    with pytest.raises(ValueError):
        strict_parse_address("0X"+hexstr)
    with pytest.raises(ValueError):
        strict_parse_address("0x0"+hexstr)
    with pytest.raises(ValueError):
        strict_parse_address("'"+hexstr+'"')
    with pytest.raises(ValueError):
        strict_parse_address("0")
    with pytest.raises(ValueError):
        strict_parse_address("")
    with pytest.raises(TypeError):
        strict_parse_address(None)
    with pytest.raises(ValueError):
        strict_parse_address(b'abc')
