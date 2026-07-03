"""
The pytest_generate_tests function we provide will get called by pytest when it's
building its list of tests to run. The metafunc object has a lot of information,
but we're using it just to get the parameter name and to generate the
parametrizations.
"""

from cards import Card


def pytest_generate_tests(metafunc):
    if "start_state" in metafunc.fixturenames:
        metafunc.parametrize("start_state", ["done", "in prog", "todo"])


def test_finish(db, start_state):
    c = Card("write a book", state=start_state)
    index = db.add_card(c)
    db.finish(index)
    card = db.get_card(index)
    assert card.state == "done"
