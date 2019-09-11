import libra
import pdb

def test_grpc():
    address = "000000000000000000000000000000000000000000000000000000000a550c18"
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    #pdb.set_trace()
    assert len(events) == 2