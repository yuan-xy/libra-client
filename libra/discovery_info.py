from canoser import Struct, Uint8
from libra.account_address import Address
from libra.crypto.x25519 import X25519_PUBLIC_KEY_LENGTH

Multiaddr = str

class DiscoveryInfo(Struct):
    """
    # A validator's discovery information, which describes how to dial the
    # validator's node and full nodes.
    #
    # Other validators will use the `validator_network_address` to dial the this
    # validator and only accept inbound connections from this validator if it's
    # authenticated to `validator_network_identity_pubkey`.
    #
    # In contrast, other full nodes and clients will use the
    # `fullnodes_network_identity_pubkey` and `fullnodes_network_address` fields
    # respectively to contact this validator.
    """
    _fields = [
        # The validator's account address.
        ("account_address", Address),
        # This static pubkey is used in the connection handshake to authenticate
        # this particular validator.
        ("validator_network_identity_pubkey", [Uint8, X25519_PUBLIC_KEY_LENGTH]),
        # Other validators can dial this validator at this multiaddress.
        ("validator_network_address", Multiaddr),
        # This static pubkey is used in the connection handshake to authenticate
        # this validator's full nodes.
        ("fullnodes_network_identity_pubkey", [Uint8, X25519_PUBLIC_KEY_LENGTH]),
        # Other full nodes and clients can dial this validator's full nodes at this
        # multiaddress.
        ("fullnodes_network_address", Multiaddr)
    ]
