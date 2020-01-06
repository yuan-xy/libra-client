from libra.account_config import *
from libra.event import *
from libra.contract_event import ContractEvent
from libra.account_address import Address
import libra
import libra_client
#import pdb


def test_event_sent():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    assert len(events) == 2
    assert events[0].transaction_version >= events[1].transaction_version
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    tag0 = contracts[0].type_tag.value
    assert tag0.address == libra.AccountConfig.core_code_address_ints()
    assert tag0.module == 'LibraAccount'
    assert tag0.name == 'SentPaymentEvent'
    assert tag0.is_pay_tag() == True
    tag1 = contracts[1].type_tag.value
    assert tag1.address == libra.AccountConfig.core_code_address_ints()
    assert tag1.module == 'LibraAccount'
    assert tag1.name == 'SentPaymentEvent'
    assert tag1.is_pay_tag() == True
    assert len(contracts[0].event_data) == 44
    assert len(contracts[0].event_data) == 44
    assert contracts[0].key == contracts[1].key
    assert contracts[0].event_seq_num-1 == contracts[1].event_seq_num
    assert len(contracts[0].event_data) == 44
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    assert aes[1].amount >0
    assert len(aes[1].account) == 32
    contract2s = [ContractEvent.from_proto_event_with_proof(x) for x in events]
    assert contract2s[0].event_data_decode.amount == aes[0].amount
    res = c.get_account_resource(address)
    assert res.sent_events.key == contracts[0].key
    assert res.sent_events.count == contracts[0].event_seq_num+1
    assert res.sequence_number >= res.sent_events.count

def test_latest_events_received():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_latest_events_received(address, 1)
    assert len(events) == 1
    assert events[0].transaction_version >= 0
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    tag0 = contracts[0].type_tag.value
    assert tag0.address == libra.AccountConfig.core_code_address_ints()
    assert tag0.module == 'LibraAccount'
    assert tag0.name == 'ReceivedPaymentEvent'
    assert len(contracts[0].event_data) == 44
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
    res = c.get_account_resource(address)
    assert res.received_events.key == contracts[0].key
    assert res.received_events.count == contracts[0].event_seq_num+1
    assert res.event_generator == 2



def test_events_received():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_events_received(address, 0, limit=1)
    assert len(events) == 1
    assert events[0].transaction_version >= 0
    contracts = [ContractEvent.from_proto(x.event) for x in events]
    tag0 = contracts[0].type_tag.value
    assert tag0.address == libra.AccountConfig.core_code_address_ints()
    assert tag0.module == 'LibraAccount'
    assert tag0.name == 'ReceivedPaymentEvent'
    assert len(contracts[0].event_data) == 44
    aes = [AccountEvent.deserialize(x.event_data) for x in contracts]
    assert aes[0].amount >0
    assert len(aes[0].account) == 32
