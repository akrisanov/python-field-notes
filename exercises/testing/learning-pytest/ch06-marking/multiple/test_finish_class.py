import pytest
from cards import Card


@pytest.mark.smoke
class TestFinish:
    def test_finish_from_todo(self, db):
        i = db.add_card(Card("foo", state="todo"))
        db.finish(i)
        c = db.get_card(i)
        assert c.state == "done"

    def test_finish_from_in_prog(self, db):
        i = db.add_card(Card("foo", state="in prog"))
        db.finish(i)
        c = db.get_card(i)
        assert c.state == "done"

    def test_finish_from_done(self, db):
        i = db.add_card(Card("foo", state="done"))
        db.finish(i)
        c = db.get_card(i)
        assert c.state == "done"
