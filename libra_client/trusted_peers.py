import toml
import os
import libra
from nacl.signing import VerifyKey
from libra.validator_verifier import ValidatorVerifier, ValidatorInfo
from canoser import hex_to_int_list

# pub struct ConsensusPeerInfo {
#     #[serde(rename = "c")]
#     pub consensus_pubkey: Ed25519PublicKey,
# }
# pub struct ConsensusPeersConfig {
#     pub peers: HashMap<String, ConsensusPeerInfo>,
# }

class ConsensusPeersConfig:
    @classmethod
    def testnet_file_path(cls):
        curdir = os.path.dirname(libra.__file__)
        return os.path.abspath((os.path.join(curdir, "consensus_peers.config.toml")))

    @classmethod
    def parse(cls, file_path):
        amap = toml.load(file_path)
        address_to_validator_info = {}
        for k, v in amap.items():
            address = bytes.fromhex(k)
            publickey = hex_to_int_list(v['c'])
            address_to_validator_info[address] = ValidatorInfo(publickey, 1)
        return ValidatorVerifier(address_to_validator_info)


