import pytest
from cards import Card, InvalidCardId


def test_start(db):
    """
    start changes state from "todo" to "in prog"
    """
    i = db.add_card(Card("foo", state="todo"))
    db.start(i)
    c = db.get_card(i)
    assert c.state == "in prog"


def test_start_non_existent(db):
    """
    Shouldn't be able to start a non-existent card.
    """
    any_number = 123  # any number will be invalid, db is empty with pytest.raises(InvalidCardId):
    db.start(any_number)
