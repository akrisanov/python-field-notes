import shlex
import pytest
from unittest import mock
from typer.testing import CliRunner

import cards
from cards.cli import app

runner = CliRunner()


def test_mock_version():
    with mock.patch.object(cards, "__version__", "1.2.3"):
        result = runner.invoke(app, ["version"])
        assert result.stdout.rstrip() == "1.2.3"


def test_mock_CardsDB():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        print()
        print(f" class:{MockCardsDB}")
        print(f"return_value:{MockCardsDB.return_value}")
        with cards.cli.cards_db() as db:
            print(f" object:{db}")


def test_mock_path():
    with mock.patch.object(cards, "CardsDB") as MockCardsDB:
        MockCardsDB.return_value.path.return_value = "/foo/"
        with cards.cli.cards_db() as db:
            print()
            print(f"{db.path=}")
            print(f"{db.path()=}")


@pytest.fixture()
def mock_cardsdb():
    with mock.patch.object(cards, "CardsDB", autospec=True) as CardsDB:
        yield CardsDB.return_value


def test_config(mock_cardsdb):
    mock_cardsdb.path.return_value = "/foo/"
    result = runner.invoke(app, ["config"])
    assert result.stdout.rstrip() == "/foo/"


def test_bad_mock():
    with mock.patch.object(cards, "CardsDB") as CardsDB:
        db = CardsDB("/some/path")
        db.path()  # good
        db.path(35)  # invalid arguments
        db.not_valid()  # invalid function


def cards_cli(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output


def test_add_with_owner(mock_cardsdb):
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    # read the documentation https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.assert_called
    mock_cardsdb.add_card.assert_called_with(expected)


def test_delete_invalid(mock_cardsdb):
    # pretend that delete_card generates an exception by
    # assigning the exception to the mock object side_effect attribute
    mock_cardsdb.delete_card.side_effect = cards.api.InvalidCardId
    out = cards_cli("delete 25")
    assert "Error: Invalid card id 25" in out
