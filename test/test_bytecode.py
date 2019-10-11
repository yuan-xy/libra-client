from libra.bytecode import *
import pytest
import pdb

def test_get_code_by_filenamet():
    code = get_code_by_filename("transaction_scripts/mint.bytecode")
    assert code == bytecode["mint"]
    assert get_transaction_name(code) == "mint_transaction"

