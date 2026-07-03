import pytest


@pytest.fixture()
def some_data():
    """Return answer to ultimate question."""
    return 42


def test_some_data(some_data):
    """Use fixture return value in a test."""
    assert some_data == 42
