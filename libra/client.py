from grpc import insecure_channel
import struct
import pdb

from libra.account_resource import AccountState, AccountResource

from libra.proto.admission_control_pb2 import SubmitTransactionRequest
from libra.proto.admission_control_pb2_grpc import AdmissionControlStub
from libra.proto.get_with_proof_pb2 import UpdateToLatestLedgerRequest
from libra.proto.transaction_pb2 import SignedTransaction, TransactionArgument

NETWORKS = {
    'testnet':{
        'host': "ac.testnet.libra.org:8000",
        'faucet_host': "faucet.testnet.libra.org"
    }
}
ACCOUNT_STATE_PATH = bytes.fromhex(
    "01217da6c6b3e19f1825cfb2676daecce3bf3de03cf26647c78df00b371b25cc97"
)

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
        resource = amap[ACCOUNT_STATE_PATH]
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
