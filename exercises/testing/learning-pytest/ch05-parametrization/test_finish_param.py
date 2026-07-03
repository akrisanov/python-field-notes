import pytest
from cards import Card


@pytest.mark.parametrize("start_state", ["done", "in prog", "todo"])
def test_finish(db, start_state):
    initial_card = Card(summary="write a book", state=start_state)
    index = db.add_card(initial_card)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
