import shlex
from typer.testing import CliRunner

import cards
from cards.cli import app

runner = CliRunner()


def cards_cli(command_string):
    command_list = shlex.split(command_string)
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output


def test_add_with_owner(cards_db):
    """
    A card shows up in the list with expected contents.
    """
    cards_cli("add some task -o brian")
    expected = cards.Card("some task", owner="brian", state="todo")
    all_cards = cards_db.list_cards()
    assert len(all_cards) == 1
    assert all_cards[0] == expected
