import pytest
from cards import Card

card_list = [
    Card("foo", state="todo"),
    pytest.param(Card("foo", state="in prog"), id="special"),  # <- explicitly set an id
    Card("foo", state="done"),
]


@pytest.mark.parametrize("starting_card", card_list, ids=lambda c: c.state)
def test_card(db, starting_card):
    index = db.add_card(starting_card)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
