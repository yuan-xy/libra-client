import requests
import time
from canoser import Uint64
import os
import json

from libra import Account, Address, AccountConfig
from libra.transaction import (
    RawTransaction, SignedTransaction, Script, TransactionPayload)
from libra_client.error import AccountError, TransactionError, VMError, LibraError, LibraNetError, TransactionTimeoutError

NETWORKS = {
    'testnet': {
        'url': "https://client.testnet.libra.org",
        'faucet_host': "http://faucet.testnet.libra.org",
        'waypoint_url': "https://developers.libra.org/testnet_waypoint.txt"
    }
}


class DictObj:
    def __init__(self, _dict):
        for key in _dict:
            value = _dict[key]
            if type(value) == dict:
                value = DictObj(value)
            setattr(self, key, value)

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def to_json_serializable(self):
        return self.__dict__

    @staticmethod
    def new(_dict):
        if _dict is None:
            return None
        return DictObj(_dict)


class Client:
    def __init__(self, network="testnet", faucet_file=None, waypoint=None):
        if network == "mainnet":
            raise LibraNetError("Mainnet is not supported currently")
        if network != "testnet":
            raise LibraNetError(f"Unknown network: {network}")
        if 'TESTNET_LOCAL' in os.environ:
            self.url = os.environ['TESTNET_LOCAL']
        else:
            self.url = NETWORKS[network]['url']
        self.do_init(faucet_file, waypoint)

    def do_init(self, faucet_file=None, waypoint=None):
        self.init_faucet_account(faucet_file)
        self.timeout = 30
        self.rpcid = 1
        self.verbose = True

    def init_faucet_account(self, faucet_file):
        if self.is_testnet():
            self.faucet_host = NETWORKS['testnet']['faucet_host']
            self.faucet_account = None
        else:
            self.faucet_account = Account.gen_faucet_account(faucet_file)

    def is_testnet(self):
        return self.url == NETWORKS['testnet']['url']

    @classmethod
    def new(cls, url, faucet_file=None, waypoint=None):
        ret = cls.__new__(cls)
        ret.url = url
        ret.do_init(faucet_file)
        return ret

    def json_rpc(self, method, params):
        headers = {'Content-Type': 'application/json'}
        cur_id = self.rpcid
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": cur_id,
        }
        data = json.dumps(payload)
        resp = requests.post(self.url, data=data, headers=headers, timeout=self.timeout)
        if resp.status_code != 200:
            raise IOError(resp.text)
        ret = json.loads(resp.text)
        if ret['id'] != cur_id:
            raise f"Json rpc id mismatch: {ret['id']} - {cur_id}"
        if 'error' in ret:
            raise LibraError(ret)
        self.rpcid += 1
        return ret['result']

    def get_account_state(self, address, retry=False):
        address = Address.normalize_to_bytes(address)
        params = [address.hex()]
        state = self.json_rpc("get_account_state", params)
        if state is None:
            raise AccountError(address)
        return DictObj(state)

    def get_account_resource(self, address, retry=False):
        return self.get_account_state(address, retry)

    def get_sequence_number(self, address, retry=False):
        try:
            state = self.get_account_resource(address, retry)
            return state.sequence_number
        except AccountError:
            return 0

    def get_balance(self, address, retry=False):
        try:
            state = self.get_account_state(address, retry)
            if state.balances:
                return state.balances[0]['amount']
            else:
                return 0
        except AccountError:
            return 0

    def get_balances(self, address, retry=False):
        state = self.get_account_state(address, retry)
        return state.balances

    def get_currencies(self):
        params = []
        return DictObj(self.json_rpc("get_currencies", params))

    def get_metadata(self):
        params = [None]
        return DictObj(self.json_rpc("get_metadata", params))

    def get_latest_ledger_info(self):
        return self.get_metadata()

    def _get_time_diff(self):
        from datetime import datetime
        meta = self.get_metadata()
        localtime = datetime.now().timestamp()
        return localtime - meta.timestamp / 1000_000

    def get_latest_transaction_version(self):
        return self.get_latest_ledger_info().version

    def get_transactions(self, start_version, limit=1, include_events=False):
        params = [start_version, limit, include_events]
        txs = self.json_rpc("get_transactions", params)
        ret = []
        for tx in txs:
            tx = DictObj(tx)
            tx.success = (tx.vm_status == 4001)
            ret.append(tx)
        return ret

    def get_transaction(self, start_version, include_events=False):
        txs = self.get_transactions(start_version, 1, include_events)
        if txs == []:
            return None
        else:
            return txs[0]

    def get_account_transaction(self, address, sequence_number, include_events=False):
        address = Address.normalize_to_bytes(address)
        params = [address.hex(), sequence_number, include_events]
        return DictObj.new(self.json_rpc("get_account_transaction", params))

    def get_events(self, key, start_sequence_number, ascending=True, limit=1):
        limit = Uint64.int_safe(limit)
        if limit == 0:
            raise ValueError(f"limit:{limit} is invalid.")
        params = [key, start_sequence_number, limit]
        events = self.json_rpc("get_events", params)
        if not ascending:
            events = reversed(events)
        return [DictObj(ev) for ev in events]

    def get_events_sent(self, address, start_sequence_number, ascending=True, limit=1):
        key = self.get_account_state(address).sent_events_key
        return self.get_events(key, start_sequence_number, ascending, limit)

    def get_events_received(self, address, start_sequence_number, ascending=True, limit=1):
        key = self.get_account_state(address).received_events_key
        return self.get_events(key, start_sequence_number, ascending, limit)

    def get_latest_events_sent(self, address, limit=1):
        # TODO: json-rpc doesn't support fetch latest events.
        return self.get_events_sent(address, 2**64 - 1, False, limit)

    def get_latest_events_received(self, address, limit=1):
        return self.get_events_received(address, 2**64 - 1, False, limit)

    def mint_coins(self, address, auth_key_prefix, micro_libra, **kwargs):
        if self.faucet_account:
            tx = self.mint_coins_with_faucet_account(address, auth_key_prefix, micro_libra, **kwargs)
            return tx.raw_txn.sequence_number
        else:
            # TODO: auth_key_prefix+address may not equal auth_key
            is_blocking = False
            if 'is_blocking' in kwargs:
                is_blocking = bool(kwargs['is_blocking'])
            return self.mint_coins_with_faucet_service(auth_key_prefix + address, micro_libra, is_blocking)

    def mint_coins_with_faucet_account(self, receiver_address, auth_key_prefix, micro_libra, **kwargs):
        script = Script.gen_mint_script(receiver_address, auth_key_prefix, micro_libra)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, **kwargs)

    def mint_coins_with_faucet_service(self, auth_key, micro_libra, is_blocking=False):
        if isinstance(auth_key, bytes):
            auth_key = auth_key.hex()
        params = {
            "amount": micro_libra,
            "auth_key": auth_key,
            "currency_code": "LBR",
        }
        resp = requests.post(self.faucet_host, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            raise IOError(
                f"Faucet service {self.faucet_host} error: {resp.status_code}, {resp.text}"
            )
        sequence_number = Uint64.int_safe(resp.text) - 1
        if is_blocking:
            self.wait_for_transaction(AccountConfig.treasury_compliance_account_address(), sequence_number)
        return sequence_number

    def wait_for_transaction(self, address, sequence_number, expiration_time=Uint64.max_value):  # noqa: C901
        max_iterations = 50
        if self.verbose:
            address_hex = address
            if isinstance(address_hex, bytes):
                address_hex = address.hex()
            print(f"waiting for {address_hex} with sequence number {sequence_number}", flush=True)
        while max_iterations > 0:
            time.sleep(1)
            max_iterations -= 1
            ret = self.get_account_transaction(address, sequence_number, True)
            if ret is not None:
                if self.verbose:
                    print(f"\ntransaction {ret.version} is stored!")
                if len(ret.events) == 0:
                    if self.verbose:
                        print("no events emitted")
                major_status = ret.vm_status
                if major_status != 4001:
                    from libra.vm_error import StatusCode
                    raise VMError(major_status, StatusCode.get_name(major_status))
                else:
                    return
            else:
                if self.verbose:
                    print(".", end='', flush=True)
        raise TransactionTimeoutError("wait_for_transaction timeout.")

    def transfer_coin(self, sender_account, receiver_address, micro_libra, **kwargs):
        script = Script.gen_transfer_script(receiver_address, micro_libra, **kwargs)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, **kwargs)

    def create_account(self, sender_account, fresh_address, auth_key_prefix, **kwargs):
        return self.mint_coins(fresh_address, auth_key_prefix, 1, **kwargs)
        # create_account script no longer exsits.
        script = Script.gen_create_account_script(fresh_address, auth_key_prefix)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, **kwargs)

    def rotate_authentication_key(self, sender_account, public_key, **kwargs):
        script = Script.gen_rotate_auth_key_script(public_key)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(sender_account, payload, **kwargs)

    def add_validator_with_faucet_account(self, validator_address, **kwargs):
        script = Script.gen_add_validator_script(validator_address)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, **kwargs)

    def remove_validator_with_faucet_account(self, validator_address, **kwargs):
        script = Script.gen_remove_validator_script(validator_address)
        payload = TransactionPayload('Script', script)
        return self.submit_payload(self.faucet_account, payload, **kwargs)

    def submit_payload(self, sender_account, payload, **kwargs):
        sequence_number = self.get_sequence_number(sender_account.address, retry=True)
        # TODO: cache sequence_number
        raw_tx = RawTransaction.new_tx(sender_account.address, sequence_number, payload, **kwargs)
        signed_txn = SignedTransaction.gen_from_raw_txn(raw_tx, sender_account)
        params = [signed_txn.serialize().hex()]
        ret = self.json_rpc("submit", params)
        if ret is not None:
            raise TransactionError(ret)
        else:
            if 'is_blocking' in kwargs and bool(kwargs['is_blocking']):
                address = bytes(raw_tx.sender)
                sequence_number = raw_tx.sequence_number
                expiration_time = raw_tx.expiration_time
                self.wait_for_transaction(address, sequence_number, expiration_time)
            return signed_txn
