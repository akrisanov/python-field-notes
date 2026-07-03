import pytest


def cut_suffix(s, suffix):
    return s[: s.rfind(suffix)]


@pytest.mark.parametrize(
    "s,suffix,expected",
    [
        ("foobar", "bar", "foo"),
        ("foobar", "boo", "foobar"),
        ("foobarbar", "bar", "foobar"),
    ],
)
def test_cust_suffix(s, suffix, expected):
    assert cut_suffix(s, suffix) == expected
