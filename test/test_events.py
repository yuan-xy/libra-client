from libra.account_config import *
from libra.event import *
from libra.contract_event import ContractEvent
from libra.account_address import Address
import libra
import libra_client
import pytest
import os

def is_local_net():
    try:
        return os.environ['TESTNET_LOCAL'].startswith("127.0.0.1")
    except KeyError:
        return False

def test_events_not_exsits():
    c = libra_client.Client("testnet")
    non_exsits_address = "0000000000000000000000000000000000000000000000000000000000000001"
    with pytest.raises(Exception) as excinfo:
        events = c.get_latest_events_sent(non_exsits_address, 2)


def test_event_sent():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_latest_events_sent(address, 2)
    # assert len(events) >= 1


def test_latest_events_received():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_latest_events_received(address, 1)
    if len(events) == 0:
        return
    assert len(events) == 1
    assert events[0].transaction_version >= 0


def test_events_received():
    address = libra.AccountConfig.association_address()
    c = libra_client.Client("testnet")
    events = c.get_events_received(address, 0, limit=1)
    if len(events) == 0:
        return
    assert len(events) == 1
    assert events[0].transaction_version >= 0
