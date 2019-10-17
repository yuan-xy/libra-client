import libra
from libra.json_print import *
import pdb


def test_print_wallet():
    wallet = libra.WalletLibrary.recover('test/test.wallet')
    assert json_dumps(wallet) == """{
    "mnemonic": "whip gain explain arrange oil siren senior cricket labor usage sport actor series cattle settle cradle hint real proud dizzy stumble amused vintage physical",
    "seed": "5ba4b8798d78c08999c6baf4e647a9218541820659b6bf11d64dae399fd209e5",
    "child_count": 2,
    "accounts.address": [
        "7af57a0c206fbcc846532f75f373b5d1db9333308dbc4673c5befbca5db60e2f",
        "f1f48f56c4deea75f4393e832edef247547eb76e1cd498c27cc972073ec4dbde"
    ]
}"""
