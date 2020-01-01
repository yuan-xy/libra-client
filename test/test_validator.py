from libra.trusted_peers import ConsensusPeersConfig
from libra.account_address import ADDRESS_LENGTH
from nacl.signing import VerifyKey
#import pdb



def test_validator():
    validator_set_file = ConsensusPeersConfig.testnet_file_path()
    validator_verifier = ConsensusPeersConfig.parse(validator_set_file)
    assert len(validator_verifier.address_to_validator_info) == 10
    assert validator_verifier.quorum_size == 7
    for k, v in validator_verifier.address_to_validator_info.items():
        assert len(k) == ADDRESS_LENGTH
        assert len(v.public_key) == 32
        assert v.voting_power == 1
