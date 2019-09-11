from grpc import insecure_channel
import struct
import pdb

from libra.account_resource import AccountState, AccountResource
from libra.account_config import AccountConfig

from libra.proto.admission_control_pb2 import SubmitTransactionRequest
from libra.proto.admission_control_pb2_grpc import AdmissionControlStub
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
from libra.proto.transaction_pb2 import SignedTransaction, TransactionArgument
from libra.proto.access_path_pb2 import AccessPath

NETWORKS = {
    'testnet':{
        'host': "ac.testnet.libra.org:8000",
        'faucet_host': "faucet.testnet.libra.org"
    }
}


class Client:
    def __init__(self, network):
        self.channel = insecure_channel(NETWORKS['testnet']['host'])
        self.stub = AdmissionControlStub(self.channel)

    def get_account_state(self, address):
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_account_state_request.address = bytes.fromhex(address)
        resp = self.stub.UpdateToLatestLedger(request)
        blob = resp.response_items[0].get_account_state_response.account_state_with_proof.blob
        amap = AccountState.deserialize(blob.blob).blob
        resource = amap[AccountConfig.ACCOUNT_RESOURCE_PATH]
        bstr = struct.pack("<{}B".format(len(resource)),*resource)
        return AccountResource.deserialize(bstr)

    def get_sequence_number(self, address):
        state = self.get_account_state(address)
        return state.sequence_number

    def get_balance(self, address):
        state = self.get_account_state(address)
        return state.balance

    def get_latest_transaction_version(self, address):
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
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_account_transaction_by_sequence_number_request.account = bytes.fromhex(address)
        item.get_account_transaction_by_sequence_number_request.sequence_number = sequence_number
        item.get_account_transaction_by_sequence_number_request.fetch_events = fetch_events
        resp = self.stub.UpdateToLatestLedger(request)
        transaction = resp.response_items[0].get_account_transaction_by_sequence_number_response
        return transaction.signed_transaction_with_proof.signed_transaction
        #Types::SignedTransactionWithProof [:version, :signed_transaction, :proof, :events]


    # Returns events specified by `access_path` with sequence number in range designated by
    # `start_seq_num`, `ascending` and `limit`. If ascending is true this query will return up to
    # `limit` events that were emitted after `start_event_seq_num`. Otherwise it will return up to
    # `limit` events in the reverse order. Both cases are inclusive.
    def get_events(self, address, path, start_sequence_number, ascending=True, limit=1):
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_events_by_event_access_path_request.access_path.address = bytes.fromhex(address)
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
