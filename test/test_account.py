from libra.account import *
from libra.account_config import AccountConfig
from libra.json_print import json_print

def test_faucet_account(capsys):
    faucet_account = Account.gen_faucet_account(None)
    assert faucet_account.address_hex == AccountConfig.association_address()
    assert faucet_account.sequence_number == 0
    assert faucet_account.status == AccountStatus.Local
    json_print(faucet_account)
    assert capsys.readouterr().out == """{
    "address": "000000000000000000000000000000000000000000000000000000000a550c18",
    "private_key": "82001573a003fd3b7fd72ffb0eaf63aac62f12deb629dca72785a66268ec758b",
    "public_key": "664f6e8f36eacb1770fa879d86c2c1d0fafea145e84fa7d671ab7a011a54d509"
}
"""
