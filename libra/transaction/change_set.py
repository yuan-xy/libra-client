from canoser import Struct
from libra.transaction.write_set import WriteSet
from libra.contract_event import ContractEvent


class ChangeSet(Struct):

    _fields = [
        ('write_set', WriteSet),
        ('events', [ContractEvent])
    ]
