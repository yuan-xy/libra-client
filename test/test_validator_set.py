from libra.validator_set import ValidatorSet


def test_validator_set_path():
    validator_set_path = [1, 146, 133, 100, 168, 65, 88, 76, 83, 113, 115, 248, 50, 183, 193, 152, 108, 246, 65, 147, 93, 224, 42, 61, 48, 107, 126, 146, 213, 178, 116, 197, 26]
    assert ValidatorSet.validator_set_path() == validator_set_path

