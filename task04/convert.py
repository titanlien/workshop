#!/usr/bin/env python3
import argparse

"""https://www.rapidtables.com/convert/number/how-number-to-roman-numerals.html"""

ROMAN_NUMERALS = [
    (1000, 'M'),
    (900, 'CM'),
    (500, 'D'),
    (400, 'CD'),
    (100, 'C'),
    (90, 'XC'),
    (50, 'L'),
    (40, 'XL'),
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
]

def int_to_roman_num(_int: int) -> str:
    """Convert a integer to a Roman numerals

    :param _int: the digital number
    """
    if (not isinstance(_int, int)):
        raise TypeError("input int must be of type int")
    return_list = []
    keeper = _int
    for integer, numeral in ROMAN_NUMERALS:
        quotient, keeper = divmod(keeper, integer)
        return_list.append(quotient * numeral)

    return ''.join(return_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="converts integer numbers into Roman numbers")
    parser.add_argument(
        "integer",
        metavar="N",
        type=int,
        choices=range(1, 999999),
        help="an natural number for webapp size, [1-9999]",
    )
    args = parser.parse_args()
    print (int_to_roman_num(args.integer))
