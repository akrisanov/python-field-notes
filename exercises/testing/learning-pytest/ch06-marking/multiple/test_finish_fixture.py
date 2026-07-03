import pytest
from cards import Card


@pytest.mark.parametrize(
    "start_state",
    [
        "todo",
        pytest.param("in prog", marks=pytest.mark.smoke),  # <- marks also takes a list
        "done",
    ],
)
def test_finish_func(db, start_state):
    i = db.add_card(Card("foo", state=start_state))
    db.finish(i)
    c = db.get_card(i)
    assert c.state == "done"
