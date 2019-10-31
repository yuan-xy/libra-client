from libra.account_config import *
from libra.event import *
from libra.account_address import Address
import libra
import pdb

core_code_address = Address.normalize_to_int_list(libra.AccountConfig.core_code_address())

def test_event_sent():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    assert len(events) == 2
    assert events[0].transaction_version >= events[1].transaction_version
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    tag0 = contracts[0].type_tag.value
    assert tag0.address == core_code_address
    assert tag0.module == 'LibraAccount'
    assert tag0.name == 'SentPaymentEvent'
    tag1 = contracts[1].type_tag.value
    assert tag1.address == core_code_address
    assert tag1.module == 'LibraAccount'
    assert tag1.name == 'SentPaymentEvent'
    assert len(contracts[0].event_data) == 40
    assert len(contracts[0].event_data) == 40
    assert contracts[0].key == contracts[1].key
    assert contracts[0].sequence_number-1 == contracts[1].sequence_number
    assert len(contracts[0].event_data) == 40
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    assert aes[1].amount >0
    assert len(aes[1].account) == 32
    res = c.get_account_resource(address)
    assert res.sent_events.key == contracts[0].key
    assert res.sent_events.count == contracts[0].sequence_number+1

def test_event_received():
    address = libra.AccountConfig.association_address()
    c = libra.Client("testnet")
    events = c.get_latest_events_received(address, 1)
    if len(events) == 0:
        #pdb.set_trace()
        return
    assert len(events) == 1
    assert events[0].transaction_version > 0
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    tag0 = contracts[0].type_tag.value
    assert tag0.address == core_code_address
    assert tag0.module == 'LibraAccount'
    assert tag0.name == 'ReceivedPaymentEvent'
    assert len(contracts[0].event_data) == 40
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    res = c.get_account_resource(address)
    assert res.received_events.key == contracts[0].key
    assert res.received_events.count == contracts[0].sequence_number+1
