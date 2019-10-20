from libra.cli.command import *

def test_params_valid():
    assert False == params_valid("", "1".split())
    assert False == params_valid("<1> ", "1 2".split())
    assert False == params_valid("<1> ", "".split())
    assert False == params_valid("<1> <2>", "1".split())
    assert False == params_valid("<1> [2]", "".split())
    assert True == params_valid("<1> [2]", "1".split())
    assert True == params_valid("<1> [2]", "1 2".split())
    assert False == params_valid("<1> [2]", "1 2 3".split())
    spec = "<account_ref_id>|<account_address> <sent|received> <start_sequence_number> <ascending=true|false> <limit>"
    assert False == params_valid(spec, "1 2 3 4".split())
    assert True == params_valid(spec, "1 2 3 4 5".split())
    assert False == params_valid(spec, "1 2 3 4 5 6".split())

def test_params_valid2():
    spec = "\n\t<sender_account_address>|<sender_account_ref_id>"\
            " <receiver_account_address>|<receiver_account_ref_id> <number_of_coins>"\
            " [gas_unit_price_in_micro_libras (default=0)] [max_gas_amount_in_micro_libras (default 140000)]"\
            " Suffix 'b' is for blocking. "
    assert False == params_valid(spec, "1 2".split())
    assert True == params_valid(spec, "1 2 3".split())
    assert True == params_valid(spec, "1 2 3 4".split())
    assert True == params_valid(spec, "1 2 3 4 5".split())
    assert False == params_valid(spec, "1 2 3 4 5 6".split())

def test_params_valid3():
    spec = "<sender_account_address>|<sender_account_ref_id> <compiled_module_path> [parameters ...]"
    assert False == params_valid(spec, "1".split())
    assert True == params_valid(spec, "1 2".split())
    assert True == params_valid(spec, "1 2 3".split())
    assert True == params_valid(spec, "1 2 3 4".split())
    assert True == params_valid(spec, "1 2 3 4 5 6 7 8 9".split())