from libra.discovery_set import DiscoverySet

def test_discovery_set():
    key = DiscoverySet.change_event_key()
    assert len(key) == 40
    assert key == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 21, 192]
