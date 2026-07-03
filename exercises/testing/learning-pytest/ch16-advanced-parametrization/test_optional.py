"""
Optional Indirect Fixture.

This technique allows us to use the same fixture that expects a value with
both parametrized and non-parametrized tests.
"""

import pytest


@pytest.fixture()
def user(request):
    role = getattr(request, "param", "visitor")  # if no param found, set it to visitor
    print(f"\nLog in as {role}")
    return role


def test_unspecified_user(user):
    ...


@pytest.mark.parametrize("user", ["admin", "team_member"], indirect=["user"])
def test_admin_and_team_member(user):
    ...
