import pytest
from cards import Card

card_list = [
    Card("foo", state="todo"),
    Card("foo", state="in prog"),
    Card("foo", state="done"),
]


def card_state(card):
    """Returns a label for a test parameter."""
    return card.state


@pytest.mark.parametrize(
    "starting_card",
    card_list,
    ids=card_state,  # <- another option is to use lambdas, like ids=lambda c: c.state
)
def test_card(db, starting_card):
    index = db.add_card(starting_card)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
