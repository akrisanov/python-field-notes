# Pytest test
from rle import rle


def test_rle():
    assert rle("mississippi") == [
        ("m", 1),
        ("i", 1),
        ("s", 2),
        ("i", 1),
        ("s", 2),
        ("i", 1),
        ("p", 2),
        ("i", 1),
    ]


def test_rle_empty():
    assert not list(rle(""))
