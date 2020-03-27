from libra.json_print import *
import libra_client
#import pdb


def test_print_wallet():
    wallet = libra_client.WalletLibrary.recover('test/test.wallet')
    assert json_dumps(wallet) == """{
    "mnemonic": "whip gain explain arrange oil siren senior cricket labor usage sport actor series cattle settle cradle hint real proud dizzy stumble amused vintage physical",
    "seed": "5ba4b8798d78c08999c6baf4e647a9218541820659b6bf11d64dae399fd209e5",
    "child_count": 2,
    "accounts.address": [
        "c3201a49948171c3fecbcba0282c89b0",
        "116998abbe30cb048b6c4d430922c9c2"
    ]
}"""
