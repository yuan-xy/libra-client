import toml
import os
import libra
from nacl.signing import VerifyKey


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
        for k, v in amap.items():
            amap[k] = VerifyKey(bytes.fromhex(v['c']))
        return amap

