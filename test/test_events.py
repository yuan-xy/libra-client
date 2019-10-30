from libra.account_config import *
from libra.event import *
import libra
import pdb

def test_event():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    assert len(events) == 2
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    assert contracts[0].key == contracts[1].key
    assert contracts[0].sequence_number-1 == contracts[1].sequence_number
    assert len(contracts[0].event_data) == 44
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    assert aes[1].amount >0
    assert len(aes[1].account) == 32
