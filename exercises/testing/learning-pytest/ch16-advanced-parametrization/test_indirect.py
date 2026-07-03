"""An indirect parameter is one that gets passed to a fixture before it gets sent to the test function.

Indirect parameters can also be used to select a subset of values from a parametrized fixture.
"""

import pytest


@pytest.fixture()
def user(request):
    role = request.param
    print(f"\nLog in as {role}")
    yield role
    print(f"\nLog out {role}")


# We can also set indirect=True if we want all parameters to be indirect.
@pytest.mark.parametrize("user", ["admin", "team_member", "visitor"], indirect=["user"])
def test_access_rights(user):
    print(f"Test access rights for {user}")
