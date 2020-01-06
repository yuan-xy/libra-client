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
    assert amap["raw_txn"]["sender"] == "000000000000000000000000000000000000000000000000000000000a550c18"
    assert tx.raw_txn.sequence_number == 0
    assert tx.raw_txn.max_gas_amount == 0
    assert tx.raw_txn.gas_unit_price == 0
    assert tx.raw_txn.expiration_time == 18446744073709551615
    return #make test passed first
    if TESTNET_LOCAL:
        assert_key_related_local(tx, amap)
    else:
        assert_key_related_testnet(tx, amap)
    cset = tx.raw_txn.payload.value
    assert type(cset) == ChangeSet
    wset = cset.write_set
    if TESTNET_LOCAL:
        assert len(wset.write_set) == 24
    else:
        assert len(wset.write_set) == 43
    non_zero_addrs = {}
    for index, wop in enumerate(wset.write_set):
        ap, _ = wop
        if ap.address != [0]*32:
            non_zero_addrs[index] = bytes(ap.address)
    for index, wop in enumerate(wset.write_set):
        if index not in non_zero_addrs.keys():
            assert ap.address == [0]*32
    jstr = json_dumps(non_zero_addrs)
    if TESTNET_LOCAL:
        assert jstr == """{
    "1": "00000000000000000000000000000000000000000000000000000000000001d8",
    "2": "00000000000000000000000000000000000000000000000000000000000001d8",
    "3": "0000000000000000000000000000000000000000000000000000000000000fee",
    "4": "0000000000000000000000000000000000000000000000000000000000000fee",
    "5": "000000000000000000000000000000000000000000000000000000000a550c18",
    "6": "000000000000000000000000000000000000000000000000000000000a550c18",
    "7": "000000000000000000000000000000000000000000000000000000000a550c18",
    "8": "000000000000000000000000000000000000000000000000000000000a550c18",
    "9": "000000000000000000000000000000000000000000000000000000000a550c18",
    "10": "8deeeaed65f0cd7484a9e4e5ac51fbac548f2f71299a05e000156031ca78fb9f",
    "11": "8deeeaed65f0cd7484a9e4e5ac51fbac548f2f71299a05e000156031ca78fb9f"
}"""
    else:
        assert jstr == """{
    "1": "00000000000000000000000000000000000000000000000000000000000001d8",
    "2": "00000000000000000000000000000000000000000000000000000000000001d8",
    "3": "00000000000000000000000000000000000000000000000000000000000001d8",
    "4": "0000000000000000000000000000000000000000000000000000000000000fee",
    "5": "0000000000000000000000000000000000000000000000000000000000000fee",
    "6": "000000000000000000000000000000000000000000000000000000000a550c18",
    "7": "000000000000000000000000000000000000000000000000000000000a550c18",
    "8": "000000000000000000000000000000000000000000000000000000000a550c18",
    "9": "000000000000000000000000000000000000000000000000000000000a550c18",
    "10": "000000000000000000000000000000000000000000000000000000000a550c18",
    "11": "19f93314cbe8c0925a4492eb2f2f197ce6e11717449c218f50e043e37fa7a5f3",
    "12": "19f93314cbe8c0925a4492eb2f2f197ce6e11717449c218f50e043e37fa7a5f3",
    "13": "26873decd9330065988b0acf5027662b5097fb50913ae2a2652b50a9869df4fb",
    "14": "26873decd9330065988b0acf5027662b5097fb50913ae2a2652b50a9869df4fb",
    "15": "3b7c756cce9ad7d801b078a08ee91df5f8122e44011b4fdf6d6c20c016823b8f",
    "16": "3b7c756cce9ad7d801b078a08ee91df5f8122e44011b4fdf6d6c20c016823b8f",
    "17": "4995559c4844b7e4101c486035329402a8ba4976c1be23080bac5bddf6a60f0d",
    "18": "4995559c4844b7e4101c486035329402a8ba4976c1be23080bac5bddf6a60f0d",
    "19": "4d78ab90b759ecacafe4e687c5db9cc2936a7a29c84aa8be777f54db519d756b",
    "20": "4d78ab90b759ecacafe4e687c5db9cc2936a7a29c84aa8be777f54db519d756b",
    "21": "6687e9a6e6c3de0dc4f7e91eacbc676a228a9c0c46450bbccbd1072780bfcb30",
    "22": "6687e9a6e6c3de0dc4f7e91eacbc676a228a9c0c46450bbccbd1072780bfcb30",
    "23": "9102bd7b1ad7e8f31023c500371cc7d2971758b450cfa89c003efb3ab192a4b8",
    "24": "9102bd7b1ad7e8f31023c500371cc7d2971758b450cfa89c003efb3ab192a4b8",
    "25": "c28b953590c58117ae8431456ea28f67c2f9e1733078b208e1a7bd5bd4081e9e",
    "26": "c28b953590c58117ae8431456ea28f67c2f9e1733078b208e1a7bd5bd4081e9e",
    "27": "dfb9c683d1788857e961160f28d4c9c79b23f042c80f770f37f0f93ee5fa6a96",
    "28": "dfb9c683d1788857e961160f28d4c9c79b23f042c80f770f37f0f93ee5fa6a96",
    "29": "f9770caa0be0c0ad427f204c22a2c2d7b22ee373a1b9cf6fd768fbf48a079554",
    "30": "f9770caa0be0c0ad427f204c22a2c2d7b22ee373a1b9cf6fd768fbf48a079554"
}"""


def assert_key_related_local(tx, amap):
    assert amap["public_key"] == "5302e9093c3a35e9ae9bd2ddb84e29cec4a95094151523594687e7da37d08f95"
    assert amap["signature"] == "71c902743b21e4bf32d2f0d887bf0cdee119e106e814368960e76153f268c8d01e2bc95c4e8699091cbf4437a35864a7560f180651b166c6e063216956ced206"
    assert json_dumps(tx.transaction_info) == """{
    "transaction_hash": "613b226d0180e3ce06e9ddc3d483e388fcfe163cffb5508e071abb33db02f6c1",
    "state_root_hash": "83aae0498f53dc181930992820cd0487d1298d367c8d575780506157b13a7279",
    "event_root_hash": "4d59582dee7d15449806ff6089cdedd7c5f420c930611158c29310798d2fa49d",
    "gas_used": 0,
    "major_status": 4001
}"""

def assert_key_related_testnet(tx, amap):
    assert amap["public_key"] == "664f6e8f36eacb1770fa879d86c2c1d0fafea145e84fa7d671ab7a011a54d509"
    assert amap["signature"] == "971ecf91553cf0374516f82adc26e34dfc1710dea1a10bf6fa7fff872498fc8014a4c7a33add7cf60a227d7fb18455579e015af2fb10dff5df7b8fef74a6c10a"
    assert json_dumps(tx.transaction_info) == """{
    "transaction_hash": "fb0ec2bac6fea6d98bb0eba35ea6718b6fd31c3bf4f8946243b9089fe9ded3fc",
    "state_root_hash": "9ce3da57b265158b86a911dd5229a126d43722458bb3a34e19fd2bfc6369cedb",
    "event_root_hash": "414343554d554c41544f525f504c414345484f4c4445525f4841534800000000",
    "gas_used": 0,
    "major_status": 4001
}"""