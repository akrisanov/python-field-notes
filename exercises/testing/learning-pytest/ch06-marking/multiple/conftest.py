import pytest
import cards


@pytest.fixture(scope="session")
def db(tmp_path_factory):
    """CardsDB object connected to a temporary database."""
    db_path = tmp_path_factory.mktemp("cards_db")
    db_ = cards.CardsDB(db_path)
    yield db_
    db_.close()
