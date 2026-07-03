import pytest
from cards import Card


def test_with_fail():
    c1 = Card("sit there", "brian")
    c2 = Card("do something", "okken")
    if c1 != c2:
        pytest.fail("they don't match")
