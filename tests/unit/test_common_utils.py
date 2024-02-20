from lambdas.utils import common


def test_safe_dict():
    # assert str_utils.convert_snake_to_camel_case('abc') == 'abc'
    assert common.SafeDict({'key': 'value'}).get_nested('missing', 'nested_key') is None
