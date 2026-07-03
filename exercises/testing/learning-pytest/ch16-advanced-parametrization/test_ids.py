import pytest
from cards import Card

card_list = [
    Card("foo", state="todo"),
    Card("foo", state="in prog"),
    Card("foo", state="done"),
]


@pytest.mark.parametrize(
    "starting_card",
    card_list,
    ids=str,  # <- ids is need for human-readable parameter names, here we basically call str(obj)
)
def test_card(db, starting_card):
    index = db.add_card(starting_card)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
