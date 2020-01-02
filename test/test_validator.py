from libra.trusted_peers import ConsensusPeersConfig
from libra.account_address import ADDRESS_LENGTH
from libra.validator_verifier import ValidatorVerifier
#import pdb



def test_validator():
    validator_set_file = ConsensusPeersConfig.testnet_file_path()
    validator_verifier = ConsensusPeersConfig.parse(validator_set_file)
    assert len(validator_verifier.address_to_validator_info) == 10
    assert validator_verifier.quorum_voting_power == 7
    assert validator_verifier.total_voting_power == 10
    for k, v in validator_verifier.address_to_validator_info.items():
        assert len(k) == ADDRESS_LENGTH
        assert len(v.public_key) == 32
        assert v.voting_power == 1

def test_empty_validator():
    validator_verifier = ValidatorVerifier({})
    assert len(validator_verifier.address_to_validator_info) == 0
    assert validator_verifier.quorum_voting_power == 0
    assert validator_verifier.total_voting_power == 0
