import toml
import os
import libra
from nacl.signing import VerifyKey
from libra.validator_verifier import ValidatorVerifier

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
        author_to_public_keys = {}
        for k, v in amap.items():
            address = bytes.fromhex(k)
            author_to_public_keys[address] = VerifyKey(bytes.fromhex(v['c']))
        return ValidatorVerifier(author_to_public_keys)


