import pytest
from cards import Card


@pytest.mark.parametrize(
    "summary, owner, state",
    [
        ("short", "First", "todo"),
        ("short", "First", "in prog"),  # ...
    ],
)
def test_add_lots(db, summary, owner, state):
    """Make sure adding to db doesn't change values."""
    i = db.add_card(Card(summary, owner=owner, state=state))
    card = db.get_card(i)
    expected = Card(summary, owner=owner, state=state)
    assert card == expected
