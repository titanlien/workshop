import pytest

from convert import int_to_roman_num


def test_int_to_roman_num():
    assert int_to_roman_num(36) == 'XXXVI', "The string should be the same"
    assert int_to_roman_num(90) == 'XC'
