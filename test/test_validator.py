from libra.trusted_peers import ConsensusPeersConfig
from libra.account_address import ADDRESS_LENGTH
from libra.validator_verifier import ValidatorSet
from nacl.signing import VerifyKey
#import pdb


def test_validator_set_path():
    validator_set_path = [1, 199, 67, 201, 192, 92, 228, 217, 21, 182, 247, 123, 112, 78, 146, 191, 135, 208, 102, 202, 138, 27, 160, 213, 102, 254, 217, 189, 145, 54, 181, 212, 21]
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
