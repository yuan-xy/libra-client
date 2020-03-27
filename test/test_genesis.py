import libra_client
from libra.transaction.change_set import ChangeSet
from libra.contract_event import ContractEvent
from libra.json_print import json_dumps
import pytest
import os
#import pdb

try:
    os.environ['TESTNET_LOCAL']
    TESTNET_LOCAL = True
except KeyError:
    TESTNET_LOCAL = False



def test_genesis():
    c = libra_client.Client("testnet")
    tx = c.get_transaction(0, True)
    assert len(tx.events) == 4
    assert tx.events[0].type_tag.value.module == "LibraAccount"
    assert tx.events[0].type_tag.value.name == "SentPaymentEvent"
    assert tx.events[1].type_tag.value.module == "LibraAccount"
    assert tx.events[1].type_tag.value.name == "ReceivedPaymentEvent"
    assert tx.events[2].type_tag.value.module == "LibraSystem"
    assert tx.events[2].type_tag.value.name == "ValidatorSetChangeEvent"
    assert tx.events[3].type_tag.value.module == "LibraSystem"
    assert tx.events[3].type_tag.value.name == "DiscoverySetChangeEvent"
    amap = tx.to_json_serializable()
    assert amap["raw_txn"]["sender"] == "0000000000000000000000000a550c18"
    assert tx.raw_txn.sequence_number == 0
    assert tx.raw_txn.max_gas_amount == 0
    assert tx.raw_txn.gas_unit_price == 0
    assert tx.raw_txn.expiration_time == 18446744073709551615
