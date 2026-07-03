from cards import Card
import pytest


def assert_identical(c1: Card, c2: Card):
    # don't include the function in a traceback
    __tracebackhide__ = True

    assert c1 == c2
    if c1.id != c2.id:
        pytest.fail(f"id's don't match: {c1.id} != {c2.id}")
    # or simply c1.id == c2.id, "id's don't match"


def test_identical():
    c1 = Card("foo", id=123)
    c2 = Card("foo", id=123)
    assert_identical(c1, c2)


def test_identical_fail():
    c1 = Card("foo", id=123)
    c2 = Card("foo", id=456)
    assert_identical(c1, c2)
