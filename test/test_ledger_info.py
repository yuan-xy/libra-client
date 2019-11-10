from libra.ledger_info import *
import libra
from datetime import datetime, timezone
import time
import pytest
#import pdb

def print_time_str(unix_timestamp):
    utc_time = datetime.fromtimestamp(unix_timestamp, timezone.utc)
    local_time = utc_time.astimezone()
    print(utc_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))
    print(local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))
    return local_time

def time_offset_in_seconds():
    return -time.timezone

def test_time():
    assert time.localtime().tm_gmtoff == time_offset_in_seconds()
    utcnow = datetime.utcnow().timestamp()
    print_time_str(utcnow)
    now = datetime.now().timestamp()
    print_time_str(now)
    diff = (now - time_offset_in_seconds()) - utcnow
    assert diff > 0
    assert diff < 1

def test_ledger_info():
    c = libra.Client("testnet")
    info = c.get_latest_ledger_info()
    assert info.version > 0
    assert len(info.transaction_accumulator_hash) == 32
    assert len(info.consensus_data_hash) == 32
    assert len(info.consensus_block_id) == 32
    assert info.timestamp_usecs > 1570_000_000_000_000
    secs = info.timestamp_usecs / 1000_000
    localtime = datetime.now().timestamp()
    diff = localtime - secs
    if diff != 0:
        print(f"localtime {localtime}, ledger_info time{secs}, diff:{diff}")
    assert abs(diff) < 5
    #assert abs(datetime.utcnow().timestamp() - secs) < 5

