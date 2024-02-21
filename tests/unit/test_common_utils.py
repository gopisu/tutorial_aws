from lambdas.utils import common


def test_safe_dict():
    assert common.SafeDict({'key': 'value'}).get_nested('missing', 'nested_key') is None
    assert common.SafeDict({'key': []}).get_nested('key', 'nested_key') is None
