from libra.bytecode import *
import pytest
#import pdb

def check_bytecode(name):
    code = get_code_by_filename(f"transaction_scripts/{name}.mv")
    assert code == bytecodes[name]
    assert get_transaction_name(code) == f"{name}_transaction"

def test_get_code_by_filename():
    check_bytecode("mint")
    check_bytecode("peer_to_peer_transfer")
    check_bytecode("create_account")
    check_bytecode("rotate_authentication_key")

