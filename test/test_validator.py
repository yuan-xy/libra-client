from libra.trusted_peers import ConsensusPeersConfig
from libra.account_address import ADDRESS_LENGTH
from libra.validator_verifier import ValidatorSet
from nacl.signing import VerifyKey
import pdb


def test_validator_set_path():
    assert ValidatorSet.validator_set_path() == [1, 155, 221, 107, 26, 67, 22, 150, 190, 138, 237, 24, 137, 186, 88, 108, 176, 160, 177, 240, 38, 243, 116, 194, 183, 136, 134, 125, 14, 39, 110, 27, 70]


def test_validator():
    validator_set_file = ConsensusPeersConfig.testnet_file_path()
    validator_verifier = ConsensusPeersConfig.parse(validator_set_file)
    assert len(validator_verifier.validators) == 10
    assert validator_verifier.quorum_size == 7
    for k, v in validator_verifier.validators.items():
        assert len(k) == ADDRESS_LENGTH
        v.__class__ == VerifyKey
        assert len(v._key) == 32
