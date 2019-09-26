from libra.cli.libra_shell import *
import libra
import pdb


def test_shell():
    parser = get_parser()
    args = parser.parse_args("")
    assert args.host == "ac.testnet.libra.org"
    assert args.port == 8000
    assert args.sync == False
    assert args.validator_set_file == None
    grpc_client = libra.Client.new(args.host, args.port, args.validator_set_file)
    assert hasattr(grpc_client, "faucet_host")
