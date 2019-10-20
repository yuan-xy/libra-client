from canoser import *
from libra.event import EventHandle
from libra.hasher import gen_hasher
from libra.account_config import AccountConfig
from io import StringIO

class AccountStateBlob:
    def __init__(self, blob):
        self.blob = blob

    @classmethod
    def from_proto(cls, proto):
        return cls(proto.blob)

    def hash(self):
        shazer = gen_hasher(b"AccountStateBlob")
        shazer.update(self.blob)
        return shazer.digest()


class AccountState(Struct):
    _fields = [
        ('ordered_map', {})
    ]

    def get_resource(self):
        resource = self.ordered_map[AccountConfig.account_resource_path()]
        if resource:
            return AccountResource.deserialize(resource)
        else:
            return None

    def to_json_serializable(self):
        amap = super().to_json_serializable()
        ar = self.get_resource()
        if ar:
            amap["Decoded_resource"] = ar.to_json_serializable()
        return amap


    def __str__(self):
        concat = StringIO()
        concat.write(super().__str__())
        ar = self.get_resource()
        if ar:
            concat.write("\nDecoded:\n")
            concat.write(ar.__str__())
        return concat.getvalue()


class AccountResource(Struct):
    _fields = [
        ('authentication_key', [Uint8]),
        ('balance', Uint64),
        ('delegated_key_rotation_capability', bool),
        ('delegated_withdrawal_capability', bool),
        ('received_events', EventHandle),
        ('sent_events', EventHandle),
        ('sequence_number', Uint64)
    ]

    @classmethod
    def get_account_resource_or_default(cls, blob):
        if blob:
            omap = AccountState.deserialize(blob.blob).ordered_map
            resource = omap[AccountConfig.account_resource_path()]
            return cls.deserialize(resource)
        else:
            return cls()

    def get_event_handle_by_query_path(self, query_path):
        if AccountConfig.account_received_event_path() == query_path:
            return self.received_events
        elif AccountConfig.account_sent_event_path() == query_path:
            return self.sent_events
        else:
            libra.proof.bail("Unrecognized query path: {}", query_path);
