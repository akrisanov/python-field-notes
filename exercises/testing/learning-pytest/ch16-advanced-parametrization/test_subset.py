"""
Indirect parameters essentially let us parametrize a fixture, while keeping the parameter
values with the test function, instead of with the fixture function. This allows different tests
to use the same fixture with different parameter values.
"""

import pytest


@pytest.fixture(params=["admin", "team_member", "visitor"])
def user(request):
    ...


def test_everyone(user):
    ...


@pytest.mark.parametrize("user", ["admin"], indirect=["user"])
def test_just_admin(user):
    ...
