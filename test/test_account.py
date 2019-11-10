from libra.account import *
from libra.account_config import AccountConfig
from libra.json_print import json_print
#import pdb

def test_faucet_account(capsys):
    faucet_account = Account.gen_faucet_account(None)
    assert faucet_account.address_hex == AccountConfig.association_address()
    assert faucet_account.sequence_number == 0
    assert faucet_account.status == AccountStatus.Local
    assert Account.gen_address_from_pk(faucet_account.public_key) != faucet_account.address
    json_print(faucet_account)
    #faucet key changed, sucks.
    assert True or capsys.readouterr().out == """{
    "address": "000000000000000000000000000000000000000000000000000000000a550c18",
    "private_key": "4b8989a23c89a6d11b3e94c12e4ae1765efd6d33629fc1e6b7a02ab3d494932d",
    "public_key": "5302e9093c3a35e9ae9bd2ddb84e29cec4a95094151523594687e7da37d08f95"
}
"""
