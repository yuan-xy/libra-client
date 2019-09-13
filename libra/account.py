from nacl.signing import SigningKey
import hashlib

class Account:
    def __init__(self, private_key):
        self._signing_key = SigningKey(private_key)
        self._verify_key = self._signing_key.verify_key
        shazer = hashlib.sha3_256()
        shazer.update(self._verify_key.encode())
        self.address = shazer.digest().hex()

    def sign(self, message):
        return self._signing_key.sign(message)

    @property
    def public_key(self):
        return self._verify_key.encode().hex()

    @property
    def private_key(self):
        return self._signing_key.encode().hex()

