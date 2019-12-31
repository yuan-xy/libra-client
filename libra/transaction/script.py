from canoser import Struct, Uint8, bytes_to_int_list, hex_to_int_list
from libra.transaction.transaction_argument import TransactionArgument, normalize_public_key
from libra.bytecode import bytecodes
from libra.account_address import Address


class Script(Struct):
    _fields = [
        ('code', [Uint8]),
        ('args', [TransactionArgument])
    ]

    @classmethod
    def gen_transfer_script(cls, receiver_address,micro_libra, metadata=None):
        if isinstance(receiver_address, bytes):
            receiver_address = bytes_to_int_list(receiver_address)
        if isinstance(receiver_address, str):
            receiver_address = hex_to_int_list(receiver_address)
        if metadata is None:
            code = bytecodes["peer_to_peer_transfer"]
            args = [
                    TransactionArgument('Address', receiver_address),
                    TransactionArgument('U64', micro_libra)
                ]
        else:
            code = bytecodes["peer_to_peer_transfer_with_metadata"]
            args = [
                    TransactionArgument('Address', receiver_address),
                    TransactionArgument('U64', micro_libra),
                    TransactionArgument('ByteArray', metadata)
                ]
        return Script(code, args)

    @classmethod
    def gen_mint_script(cls, receiver_address,micro_libra):
        receiver_address = Address.normalize_to_int_list(receiver_address)
        code = bytecodes["mint"]
        args = [
                TransactionArgument('Address', receiver_address),
                TransactionArgument('U64', micro_libra)
            ]
        return Script(code, args)

    @classmethod
    def gen_create_account_script(cls, fresh_address, initial_balance=0):
        fresh_address = Address.normalize_to_int_list(fresh_address)
        code = bytecodes["create_account"]
        args = [
                TransactionArgument('Address', fresh_address),
                TransactionArgument('U64', initial_balance)
            ]
        return Script(code, args)

    @classmethod
    def gen_rotate_auth_key_script(cls, public_key):
        key = normalize_public_key(public_key)
        code = bytecodes["rotate_authentication_key"]
        args = [
                TransactionArgument('ByteArray', key)
            ]
        return Script(code, args)

    @classmethod
    def gen_rotate_consensus_pubkey_script(cls, public_key):
        key = normalize_public_key(public_key)
        code = bytecodes["rotate_consensus_pubkey"]
        args = [
                TransactionArgument('ByteArray', key)
            ]
        return Script(code, args)


    @classmethod
    def gen_add_validator_script(cls, address):
        address = Address.normalize_to_int_list(address)
        code = bytecodes["add_validator"]
        args = [
                TransactionArgument('Address', address)
            ]
        return Script(code, args)


    @classmethod
    def gen_remove_validator_script(cls, address):
        address = Address.normalize_to_int_list(address)
        code = bytecodes["remove_validator"]
        args = [
                TransactionArgument('Address', address)
            ]
        return Script(code, args)


    @classmethod
    def gen_register_validator_script(cls,
        consensus_pubkey,
        validator_network_signing_pubkey,
        validator_network_identity_pubkey,
        validator_network_address,
        fullnodes_network_identity_pubkey,
        fullnodes_network_address
        ):
        validator_network_address = Address.normalize_to_int_list(validator_network_address)
        fullnodes_network_address = Address.normalize_to_int_list(fullnodes_network_address)
        consensus_pubkey = normalize_public_key(consensus_pubkey)
        validator_network_signing_pubkey = normalize_public_key(validator_network_signing_pubkey)
        validator_network_identity_pubkey = normalize_public_key(validator_network_identity_pubkey)
        fullnodes_network_identity_pubkey = normalize_public_key(fullnodes_network_identity_pubkey)
        code = bytecodes["register_validator"]
        args = [
                TransactionArgument('ByteArray', consensus_pubkey),
                TransactionArgument('ByteArray', validator_network_signing_pubkey),
                TransactionArgument('ByteArray', validator_network_identity_pubkey),
                TransactionArgument('Address', validator_network_address),
                TransactionArgument('ByteArray', fullnodes_network_identity_pubkey),
                TransactionArgument('Address', fullnodes_network_address)
            ]
        return Script(code, args)


    @staticmethod
    def get_script_bytecode(script_name):
        return bytecodes[script_name]