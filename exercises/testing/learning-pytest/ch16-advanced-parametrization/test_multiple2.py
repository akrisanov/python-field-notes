import pytest
from cards import Card

# 2 x 2 x 3 = 12 test cases
states = ["todo", "in prog"]
owners = ["First", "First"]
summaries = ["short", "short"]


@pytest.mark.parametrize("state", states)
@pytest.mark.parametrize("owner", owners)
@pytest.mark.parametrize("summary", summaries)
def test_add_lots(db, summary, owner, state):
    """Make sure adding to db doesn't change values."""
    i = db.add_card(Card(summary, owner=owner, state=state))
    card = db.get_card(i)
    expected = Card(summary, owner=owner, state=state)
    assert card == expected
