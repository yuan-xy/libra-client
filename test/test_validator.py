from libra.trusted_peers import ConsensusPeersConfig
from libra.account_address import ADDRESS_LENGTH
from libra.validator_verifier import ValidatorSet
from nacl.signing import VerifyKey
#import pdb


def test_validator_set_path():
    validator_set_path = [1, 146, 133, 100, 168, 65, 88, 76, 83, 113, 115, 248, 50, 183, 193, 152, 108, 246, 65, 147, 93, 224, 42, 61, 48, 107, 126, 146, 213, 178, 116, 197, 26]
    assert ValidatorSet.validator_set_path() == validator_set_path


def test_validator():
    validator_set_file = ConsensusPeersConfig.testnet_file_path()
    validator_verifier = ConsensusPeersConfig.parse(validator_set_file)
    assert len(validator_verifier.validators) == 10
    assert validator_verifier.quorum_size == 7
    for k, v in validator_verifier.validators.items():
        assert len(k) == ADDRESS_LENGTH
        v.__class__ == VerifyKey
        assert len(v._key) == 32
