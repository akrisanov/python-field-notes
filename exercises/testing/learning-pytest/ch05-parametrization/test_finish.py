from cards import Card


def test_finish_from_in_prog(db):
    index = db.add_card(Card("second edition", state="in prog"))
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"


def test_finish_from_done(db):
    index = db.add_card(Card("write a book", state="done"))
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"


def test_finish_from_todo(db):
    index = db.add_card(Card("create a course", state="todo"))
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
