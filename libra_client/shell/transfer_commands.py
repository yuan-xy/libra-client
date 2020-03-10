from canoser import Uint64
from libra_client.cli.command import *


class TransferCommand(Command):
    def get_aliases(self):
        return ["transfer", "transferb", "t", "tb"]

    def get_params_help(self):
        return ("\n\t<sender_account_address>|<sender_account_ref_id>"
         " <receiver_account_address>|<receiver_account_ref_id> <number_of_coins>"
         " [metadata]"
         " [gas_unit_price_in_micro_libras (default=0)] [max_gas_amount_in_micro_libras (default 140000)]"
         " Suffix 'b' is for blocking. ")

    def get_description(self):
        return "Transfer coins (in libra) from account to another."

    def execute(self, client, params, **kwargs):
        if len(params) < 4 or len(params) > 7:
            self.print_params_help()
            return
        if len(params) == 5:
            metadata = hex_to_int_list(params[4])
        else:
            metadata = None
        if len(params) == 6:
            gas_unit_price_in_micro_libras = Uint64.int_safe(params[5])
        else:
            gas_unit_price_in_micro_libras = 0
        if len(params) == 7:
            max_gas_amount_in_micro_libras = Uint64.int_safe(params[6])
        else:
            max_gas_amount_in_micro_libras = 400_000
        print(">> Transferring")
        is_blocking = blocking_cmd(params[0])
        sequence_number = client.transfer_coins(params[1], params[2], params[3],
            max_gas_amount_in_micro_libras, gas_unit_price_in_micro_libras, is_blocking, metadata)
        if is_blocking:
            print("Finished transaction!")
        else:
            print("Transaction submitted to validator")
        print(
            "To query for transaction status, run: query txn_acc_seq {} {} \
            <fetch_events=true|false>".format(
            params[1], sequence_number
            )
        )


