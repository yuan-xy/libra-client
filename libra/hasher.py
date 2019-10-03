from libra.key_factory import new_sha3_256

LIBRA_HASH_SUFFIX = b"@@$$LIBRA$$@@";

def hash_seed(clazz):
    sha3 = new_sha3_256()
    sha3.update(clazz+LIBRA_HASH_SUFFIX)
    return sha3.digest()

def raw_tx_hash(raw_tx):
    raw_txn_bytes = raw_tx.serialize()
    salt = hash_seed(b"RawTransaction")
    shazer = new_sha3_256()
    shazer.update(salt)
    shazer.update(raw_txn_bytes)
    return shazer.digest()

def ledger_info_hash(ledger_info):
    ledger_info_bytes = ledger_info.serialize()
    salt = hash_seed(b"LedgerInfo")
    shazer = new_sha3_256()
    shazer.update(salt)
    shazer.update(ledger_info_bytes)
    return shazer.digest()
