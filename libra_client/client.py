from grpc import insecure_channel
import requests
import time
from canoser import Uint64
import os

from libra import Account, Address, AccountConfig, AccountState, AccountResource
from libra.transaction import (
    Version, Transaction, RawTransaction, SignedTransaction, Script, TransactionPayload, TransactionInfo)
from libra.ledger_info import LedgerInfo
from libra.get_with_proof import verify
from libra.contract_event import ContractEvent
from libra.validator_change import VerifierType, ValidatorChangeProof
from libra_client.error import LibraError, AccountError, TransactionError, AdmissionControlError, VMError, MempoolError, LibraNetError, TransactionTimeoutError

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


class TrustedState:
    def __init__(self, version : Version, verifier : VerifierType, latest_epoch_change_li=None):
        self.version = version
        self.verifier = verifier
        self.latest_epoch_change_li = latest_epoch_change_li


class Client:
    def __init__(self, network="testnet", faucet_file=None, waypoint=None):
        if network == "mainnet":
            raise LibraNetError("Mainnet is not supported currently")
        if network != "testnet":
            raise LibraNetError(f"Unknown network: {network}")
        if 'TESTNET_LOCAL' in os.environ:
            test_hosts = os.environ['TESTNET_LOCAL'].split(";")
            self.host = test_hosts[0]
            self.port = int(test_hosts[1])
        else:
            self.host = NETWORKS[network]['host']
            self.port = NETWORKS[network]['port']
        self.do_init(faucet_file, waypoint)

    def do_init(self, faucet_file=None, waypoint=None):
        self.init_grpc()
        self.init_faucet_account(faucet_file)
        self.init_trusted_state(waypoint)
        self.timeout = 30
        self.verbose = True

    def init_trusted_state(self, waypoint):
        if waypoint is None:
            from libra.crypto_proxies import EpochInfo
            self.state = TrustedState(0, VerifierType('TrustedVerifier', EpochInfo.empty()))
        else:
            self.state = TrustedState(waypoint.version, VerifierType('Waypoint', waypoint))

    def init_grpc(self):
        #TODO: should check under ipv6, add [] around ipv6 host
        self.channel = insecure_channel(f"{self.host}:{self.port}")
        self.stub = AdmissionControlStub(self.channel)

    def init_faucet_account(self, faucet_file):
        if self.is_testnet():
            self.faucet_host = NETWORKS['testnet']['faucet_host']
            self.faucet_account = None
        else:
            self.faucet_account = Account.gen_faucet_account(faucet_file)

    def is_testnet(self):
        return self.host == NETWORKS['testnet']['host']

    @classmethod
    def new(cls, host, port, faucet_file=None, waypoint=None):
        if port == 0:
            try:
                tests = os.environ['TESTNET_LOCAL'].split(";")
                host = tests[0]
                port = int(tests[1])
            except KeyError:
                port = 8000
        ret = cls.__new__(cls)
        ret.host = host
        if isinstance(port, str):
            port = int(port)
        if port <=0 or port > 65535:
            raise LibraNetError("port must be between 1 and 65535")
        ret.port = port
        ret.do_init(faucet_file)
        return ret


    def get_account_blob(self, address):
        address = Address.normalize_to_bytes(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_account_state_request.address = address
        resp = self.get_with_proof(request)
        blob = resp.response_items[0].get_account_state_response.account_state_with_proof.blob
        version = resp.ledger_info_with_sigs.ledger_info.version
        return (blob, version)

    def get_account_state(self, address, retry=False):
        try:
            blob, version = self.get_account_blob(address)
        except Exception:
            if retry:
                blob, version = self.get_account_blob(address)
            else:
                raise
        if len(blob.__str__()) == 0:
            #TODO: bad smell
            raise AccountError("Account state blob is empty.")
        return AccountState.deserialize(blob.blob)

    def get_account_resource(self, address, retry=False):
        state = self.get_account_state(address, retry)
        return state.get_account_resource()

    def get_sequence_number(self, address, retry=False):
        try:
            state = self.get_account_resource(address, retry)
            return state.sequence_number
        except AccountError:
            return 0

    def get_balance(self, address, retry=False):
        try:
            state = self.get_account_state(address, retry)
            return state.get_balance_resource().coin
        except AccountError:
            return 0

    def get_with_proof(self, request):
        request.client_known_version = self.state.version
        try:
            resp = self.stub.UpdateToLatestLedger(request, timeout=self.timeout)
        except Exception as err:
            if err.__class__.__name__ == '_Rendezvous' and \
                err.details().find("other accumulator is bigger than this") != -1:
                #Testnet reset, so clear old state
                self.init_trusted_state(None)
            raise
        new_epoch_info = verify(self.state.verifier, request, resp)
        if new_epoch_info is not None:
            if self.verbose:
                print(f"Trusted epoch change to :{new_epoch_info}")
            self.state.verifier = VerifierType('TrustedVerifier',new_epoch_info)
            vcp = ValidatorChangeProof.from_proto(resp.validator_change_proof)
            self.state.latest_epoch_change_li = vcp.ledger_info_with_sigs[-1]
        self.state.version = resp.ledger_info_with_sigs.ledger_info.version
        self.latest_time = resp.ledger_info_with_sigs.ledger_info.timestamp_usecs
        return resp

    def get_latest_ledger_info(self):
        request = UpdateToLatestLedgerRequest()
        resp = self.get_with_proof(request)
        return resp.ledger_info_with_sigs.ledger_info

    def _get_time_diff(self):
        from datetime import datetime
        info = self.get_latest_ledger_info()
        localtime = datetime.now().timestamp()
        return localtime - info.timestamp_usecs / 1000_000

    def get_latest_transaction_version(self):
        return self.get_latest_ledger_info().version

    def _get_txs(self, start_version, limit=1, fetch_events=False):
        start_version = Uint64.int_safe(start_version)
        limit = Uint64.int_safe(limit)
        if limit == 0:
            raise ValueError(f"limit:{limit} is invalid.")
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_transactions_request.start_version = start_version
        item.get_transactions_request.limit = limit
        item.get_transactions_request.fetch_events = fetch_events
        return (request, self.get_with_proof(request))

    def get_transactions_proto(self, start_version, limit=1, fetch_events=False):
        request, resp = self._get_txs(start_version, limit, fetch_events)
        txnp = resp.response_items[0].get_transactions_response.txn_list_with_proof
        if txnp.first_transaction_version.value != int(start_version):
            raise AssertionError(f"first_transaction_version:{txnp.first_transaction_version.value} != start_version:{start_version}")
        return (txnp.transactions, txnp.events_for_versions)

    def get_transactions(self, start_version, limit=1, fetch_events=False):
        _req, resp = self._get_txs(start_version, limit, fetch_events)
        txnp = resp.response_items[0].get_transactions_response.txn_list_with_proof
        if len(txnp.transactions) == 0:
            return []
        if txnp.first_transaction_version.value != int(start_version):
            raise AssertionError(f"first_transaction_version:{txnp.first_transaction_version.value} != start_version:{start_version}")
        txs = [Transaction.deserialize(x.transaction).value for x in txnp.transactions]
        infos = [TransactionInfo.from_proto(x) for x in txnp.proof.transaction_infos]
        for tx, info in zip(txs, infos):
            tx.transaction_info = info
        if fetch_events:
            for tx, event_list in zip(txs, txnp.events_for_versions.events_for_version):
                tx.events = [ContractEvent.from_proto(x) for x in event_list.events]
        return txs

    def get_transaction(self, start_version, fetch_events=False):
        txs = self.get_transactions(start_version, 1, fetch_events)
        if txs == []:
            return None
        else:
            return txs[0]

    def get_account_transaction_proto(self, address, sequence_number, fetch_events=False):
        address = Address.normalize_to_bytes(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        itemreq = item.get_account_transaction_by_sequence_number_request
        itemreq.account = address
        itemreq.sequence_number = sequence_number
        itemreq.fetch_events = fetch_events
        resp = self.get_with_proof(request)
        usecs = resp.ledger_info_with_sigs.ledger_info.timestamp_usecs
        transaction = resp.response_items[0].get_account_transaction_by_sequence_number_response
        return (transaction.transaction_with_proof, usecs)

    # Returns events specified by `access_path` with sequence number in range designated by
    # `start_seq_num`, `ascending` and `limit`. If ascending is true this query will return up to
    # `limit` events that were emitted after `start_event_seq_num`. Otherwise it will return up to
    # `limit` events in the reverse order. Both cases are inclusive.
    def get_events(self, address, path, start_sequence_number, ascending=True, limit=1):
        limit = Uint64.int_safe(limit)
        if limit == 0:
            raise ValueError(f"limit:{limit} is invalid.")
        address = Address.normalize_to_bytes(address)
        request = UpdateToLatestLedgerRequest()
        item = request.requested_items.add()
        item.get_events_by_event_access_path_request.access_path.address = address
        item.get_events_by_event_access_path_request.access_path.path = path
        item.get_events_by_event_access_path_request.start_event_seq_num = start_sequence_number
        item.get_events_by_event_access_path_request.ascending = ascending
        item.get_events_by_event_access_path_request.limit = limit
        resp = self.get_with_proof(request)
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


    def mint_coins(self, address, auth_key_prefix, micro_libra, is_blocking=False):
        if self.faucet_account:
            tx = self.mint_coins_with_faucet_account(address, auth_key_prefix, micro_libra, is_blocking)
            return tx.raw_txn.sequence_number
        else:
            return self.mint_coins_with_faucet_service(address, micro_libra, is_blocking)

    def mint_coins_with_faucet_account(self, receiver_address, auth_key_prefix, micro_libra, is_blocking=False):
        script = Script.gen_mint_script(receiver_address, auth_key_prefix, micro_libra)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, is_blocking=is_blocking)

    def mint_coins_with_faucet_service(self, receiver, micro_libra, is_blocking=False):
        url = "http://{}?amount={}&address={}".format(self.faucet_host, micro_libra, receiver)
        resp = requests.post(url, timeout=self.timeout)
        if resp.status_code != 200:
            raise IOError(
                f"Faucet service {self.faucet_host} error: {resp.status_code}, {resp.text}"
            )
        sequence_number = Uint64.int_safe(resp.text) - 1
        if is_blocking:
            self.wait_for_transaction(AccountConfig.association_address(), sequence_number)
        return sequence_number

    def wait_for_transaction(self, address, sequence_number, expiration_time=Uint64.max_value):
        max_iterations = 50
        if self.verbose:
            print(f"waiting for {address} with sequence number {sequence_number}", flush=True)
        while max_iterations > 0:
            time.sleep(1)
            max_iterations -= 1
            transaction, usecs = self.get_account_transaction_proto(address, sequence_number, True)
            if transaction.HasField("events"):
                if self.verbose:
                    print(f"\ntransaction {transaction.version} is stored!")
                if len(transaction.events.events) == 0:
                    if self.verbose:
                        print("no events emitted")
                major_status = transaction.proof.transaction_info.major_status
                if major_status != 4001:
                    from libra.vm_error import StatusCode
                    raise VMError(major_status, StatusCode.get_name(major_status))
                else:
                    return
            else:
                if expiration_time <= (usecs // 1000_000):
                    raise TransactionTimeoutError("Transaction expired.")
                if self.verbose:
                    print(".", end='', flush=True)
        raise TransactionTimeoutError("wait_for_transaction timeout.")

    def transfer_coin(self, sender_account, receiver_address, micro_libra,
        max_gas=400_000, unit_price=0, is_blocking=False, txn_expiration=100, metadata=None):
        script = Script.gen_transfer_script(receiver_address,micro_libra, metadata)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, max_gas, unit_price,
            is_blocking, txn_expiration)

    def create_account(self, sender_account, fresh_address, auth_key_prefix, is_blocking=True):
        script = Script.gen_create_account_script(fresh_address, auth_key_prefix)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, is_blocking=is_blocking)

    def rotate_authentication_key(self, sender_account, public_key, is_blocking=True):
        script = Script.gen_rotate_auth_key_script(public_key)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, is_blocking=is_blocking)

    def add_validator_with_faucet_account(self, validator_address, is_blocking=True):
        script = Script.gen_add_validator_script(validator_address)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, is_blocking=is_blocking)

    def remove_validator_with_faucet_account(self, validator_address, is_blocking=True):
        script = Script.gen_remove_validator_script(validator_address)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, is_blocking=is_blocking)

    def register_validator_with_faucet_account(self, consensus_pubkey,
        validator_network_signing_pubkey,
        validator_network_identity_pubkey,
        validator_network_address,
        fullnodes_network_identity_pubkey,
        fullnodes_network_address,
        is_blocking=True):
        script = Script.gen_register_validator_script(consensus_pubkey,
            validator_network_signing_pubkey,
            validator_network_identity_pubkey,
            validator_network_address,
            fullnodes_network_identity_pubkey,
            fullnodes_network_address)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, is_blocking=is_blocking)


    def submit_payload(self, sender_account, payload,
        max_gas=400_000, unit_price=0, is_blocking=False, txn_expiration=100):
        sequence_number = self.get_sequence_number(sender_account.address, retry=True)
        #TODO: cache sequence_number
        raw_tx = RawTransaction.new_tx(sender_account.address, sequence_number,
            payload, max_gas, unit_price, txn_expiration)
        signed_txn = SignedTransaction.gen_from_raw_txn(raw_tx, sender_account)
        self.submit_signed_txn(signed_txn, is_blocking)
        return signed_txn

    def submit_signed_txn(self, signed_txn, is_blocking=False):
        request = SubmitTransactionRequest()
        request.transaction.txn_bytes = signed_txn.serialize()
        return self.submit_transaction(request, signed_txn, is_blocking)


    def submit_transaction(self, request, signed_txn, is_blocking):
        resp = self.submit_transaction_non_block(request)
        if is_blocking:
            raw_tx = signed_txn.raw_txn
            address = bytes(raw_tx.sender)
            sequence_number = raw_tx.sequence_number
            expiration_time = raw_tx.expiration_time
            self.wait_for_transaction(address, sequence_number, expiration_time)
        return resp

    def submit_transaction_non_block(self, request):
        resp = self.stub.SubmitTransaction(request, timeout=self.timeout)
        status = resp.WhichOneof('status')
        if status == 'ac_status':
            if resp.ac_status.code == AdmissionControlStatusCode.Accepted:
                return resp
            else:
                raise AdmissionControlError(resp.ac_status.code, resp.ac_status.message)
        elif status == 'vm_status':
            from libra.vm_error import VMStatus
            vms = VMStatus.from_proto(resp.vm_status)
            raise VMError(vms.major_status, vms.err_msg())
        elif status == 'mempool_status':
            raise MempoolError(resp.mempool_status.code, resp.mempool_status.message)
        else:
            raise AssertionError(f"Unknown Error: {resp}")
        raise AssertionError("unreacheable")
