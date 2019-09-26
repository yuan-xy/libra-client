from grpc import insecure_channel
from nacl.signing import VerifyKey
import struct
import requests
import time

from libra.account_resource import AccountState, AccountResource
from libra.account_config import AccountConfig
from libra.transaction import *
from libra.key_factory import new_sha3_256
from libra.trusted_peers import ConsensusPeersConfig


from libra.proto.admission_control_pb2 import SubmitTransactionRequest, AdmissionControlStatusCode
from libra.proto.admission_control_pb2_grpc import AdmissionControlStub
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest

NETWORKS = {
    'testnet':{
        'host': "ac.testnet.libra.org",
        'port': 8000,
        'faucet_host': "faucet.testnet.libra.org"
    }
}

class LibraError(Exception):
    pass

class AccountError(LibraError):
    pass

class TransactionError(LibraError):
    pass

class LibraNetError(LibraError):
    pass

class Client:
    def __init__(self, network="testnet", validator_set_file=None):
        if network == "mainnet":
            raise LibraNetError("Mainnet is not supported currently")
        if network != "testnet":
            raise LibraNetError(f"Unknown network: {network}")
        self.host = NETWORKS[network]['host']
        self.port = NETWORKS[network]['port']
        self.init_validators(validator_set_file)
        self.init_grpc()

    def init_grpc(self):
        #TODO: should check under ipv6, add [] around ipv6 host
        self.channel = insecure_channel(f"{self.host}:{self.port}")
        self.stub = AdmissionControlStub(self.channel)
        if self.is_testnet():
            self.faucet_host = NETWORKS['testnet']['faucet_host']

    def is_testnet(self):
        return self.host == NETWORKS['testnet']['host']

    def init_validators(self, validator_set_file):
        if self.is_testnet() and validator_set_file is None:
            validator_set_file = ConsensusPeersConfig.testnet_file_path()
        if validator_set_file is None:
            raise LibraError("Validator_set_file is required except testnet.")
        self.validators = ConsensusPeersConfig.parse(validator_set_file)

    @classmethod
    def new(cls, host, port, validator_set_file):
        ret = cls.__new__(cls)
        ret.host = host
        if isinstance(port, str):
            port = int(port)
        if port <=0 or port > 65535:
            raise LibraNetError("port must be between 1 and 65535")
        ret.port = port
        ret.init_validators(validator_set_file)
        ret.init_grpc()
        return ret


    def get_account_blob(self, address):
        if isinstance(address, str):
            address = bytes.fromhex(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_account_state_request.address = address
        resp = self.stub.UpdateToLatestLedger(request)
        blob = resp.response_items[0].get_account_state_response.account_state_with_proof.blob
        version = resp.ledger_info_with_sigs.ledger_info.version
        return (blob, version)

    def get_account_state(self, address):
        blob, version = self.get_account_blob(address)
        if len(blob.__str__()) == 0:
            #TODO: bad smell
            raise AccountError("Account state blob is empty.")
        return AccountState.deserialize(blob.blob).blob

    def get_account_resource(self, address):
        amap = self.get_account_state(address)
        resource = amap[AccountConfig.ACCOUNT_RESOURCE_PATH]
        bstr = struct.pack("<{}B".format(len(resource)),*resource)
        return AccountResource.deserialize(bstr)

    def get_sequence_number(self, address):
        state = self.get_account_resource(address)
        return state.sequence_number

    def get_balance(self, address):
        state = self.get_account_resource(address)
        return state.balance

    def get_latest_transaction_version(self):
        request = UpdateToLatestLedgerRequest()
        resp = self.stub.UpdateToLatestLedger(request)
        return resp.ledger_info_with_sigs.ledger_info.version

    def get_transactions(self, start_version, limit=1, fetch_events=False):
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_transactions_request.start_version = start_version
        item.get_transactions_request.limit = limit
        item.get_transactions_request.fetch_events = fetch_events
        resp = self.stub.UpdateToLatestLedger(request)
        txnp = resp.response_items[0].get_transactions_response.txn_list_with_proof
        return txnp.transactions

    def get_transaction(self, start_version):
        return self.get_transactions(start_version)[0]

    def get_account_transaction(self, address, sequence_number, fetch_events=False):
        if isinstance(address, str):
            address = bytes.fromhex(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_account_transaction_by_sequence_number_request.account = address
        item.get_account_transaction_by_sequence_number_request.sequence_number = sequence_number
        item.get_account_transaction_by_sequence_number_request.fetch_events = fetch_events
        resp = self.stub.UpdateToLatestLedger(request)
        transaction = resp.response_items[0].get_account_transaction_by_sequence_number_response
        return transaction.signed_transaction_with_proof
        #Types::SignedTransactionWithProof [:version, :signed_transaction, :proof, :events]


    # Returns events specified by `access_path` with sequence number in range designated by
    # `start_seq_num`, `ascending` and `limit`. If ascending is true this query will return up to
    # `limit` events that were emitted after `start_event_seq_num`. Otherwise it will return up to
    # `limit` events in the reverse order. Both cases are inclusive.
    def get_events(self, address, path, start_sequence_number, ascending=True, limit=1):
        if isinstance(address, str):
            address = bytes.fromhex(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_events_by_event_access_path_request.access_path.address = address
        item.get_events_by_event_access_path_request.access_path.path = path
        item.get_events_by_event_access_path_request.start_event_seq_num = start_sequence_number
        item.get_events_by_event_access_path_request.ascending = ascending
        item.get_events_by_event_access_path_request.limit = limit
        resp = self.stub.UpdateToLatestLedger(request)
        return resp.response_items[0].get_events_by_event_access_path_response.events_with_proof

    def get_events_sent(self, address, start_sequence_number, ascending=True, limit=1):
      path = AccountConfig.account_sent_event_path()
      return self.get_events(address, path, start_sequence_number, ascending, limit)

    def get_events_received(self, address, start_sequence_number, ascending=True, limit=1):
      path = AccountConfig.account_received_event_path()
      return self.get_events(address, path, start_sequence_number, ascending, limit)


    def get_latest_events_sent(self, address, limit=1):
        return self.get_events_sent(address, 2**64-1, False, limit)


    def get_latest_events_received(self, address, limit=1):
        return self.get_events_received(address, 2**64-1, False, limit)


    def mint_coins_with_faucet_service(self, receiver, micro_libra, is_blocking=False):
        url = "http://{}?amount={}&address={}".format(self.faucet_host, micro_libra, receiver)
        resp = requests.post(url)
        if resp.status_code != 200:
            raise IOError(
                "Failed to send request to faucent service: {}".format(self.faucet_host)
            )
        sequence_number = int(resp.text)
        if is_blocking:
            self.wait_for_transaction(AccountConfig.association_address(), sequence_number)
        return sequence_number

    def wait_for_transaction(self, address, sequence_number):
        max_iterations = 50
        print("waiting", flush=True)
        while max_iterations > 0:
            time.sleep(1)
            max_iterations -= 1
            transaction = self.get_account_transaction(address, sequence_number, True)
            if transaction.HasField("events"):
                print("transaction is stored!")
                if len(transaction.events.events) == 0:
                    print("no events emitted")
                return
            else:
                print(".", end='', flush=True)
        print("wait_for_transaction timeout.\n")

    def transfer_coin(self, sender_account, receiver_address, micro_libra,
        max_gas=140_000, unit_price=0, is_blocking=False):
        sequence_number = self.get_sequence_number(sender_account.address)
        raw_tx = RawTransaction.gen_transfer_transaction(sender_account.address, sequence_number,
            receiver_address, micro_libra, max_gas, unit_price)
        raw_txn_bytes = raw_tx.serialize()
        tx_hash = Client.raw_tx_hash(raw_txn_bytes)
        signature = sender_account.sign(tx_hash)[:64]
        signed_txn = SignedTransaction.new_for_bytes_key(raw_tx, sender_account.public_key, signature)
        request = SubmitTransactionRequest()
        request.signed_txn.signed_txn = signed_txn.serialize()
        return self.submit_transaction(request, sender_account.address, sequence_number, is_blocking)

    @staticmethod
    def raw_tx_hash_seed():
        sha3 = new_sha3_256()
        RAW_TRANSACTION_HASHER = b"RawTransaction"
        LIBRA_HASH_SUFFIX = b"@@$$LIBRA$$@@";
        sha3.update(RAW_TRANSACTION_HASHER+LIBRA_HASH_SUFFIX)
        return sha3.digest()

    @staticmethod
    def raw_tx_hash(raw_txn_bytes):
        salt = Client.raw_tx_hash_seed()
        shazer = new_sha3_256()
        shazer.update(salt)
        shazer.update(raw_txn_bytes)
        return shazer.digest()

    @staticmethod
    def verify_transaction(message, public_key, signature):
        vkey = VerifyKey(bytes(public_key))
        vkey.verify(message, bytes(signature))


    def submit_transaction(self, request, address, sequence_number, is_blocking):
        resp = self.submit_transaction_non_block(request)
        if is_blocking:
            self.wait_for_transaction(address, sequence_number)
        return resp


    def submit_transaction_non_block(self, request):
        resp = self.stub.SubmitTransaction(request)
        status = resp.WhichOneof('status')
        if status == 'ac_status':
            if resp.ac_status.code == AdmissionControlStatusCode.Accepted:
                return resp
            else:
                raise TransactionError(f"Status code: {resp.ac_status.code}")
        elif status == 'vm_status':
            raise TransactionError(resp.vm_status.__str__())
        elif status == 'mempool_status':
            raise TransactionError(resp.mempool_status.__str__())
        else:
            raise TransactionError(f"Unknown Error: {resp}")
        raise AssertionError("unreacheable")