import pytest
from cards import Card


@pytest.fixture(params=["done", "in prog", "todo"])
def start_state(request):
    return request.param  # <- "done", "in prog", "todo"


def test_finish(db, start_state):
    c = Card(summary="write a book", state=start_state)
    index = db.add_card(c)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
