from packaging.version import parse
from cards import Card
import pytest
import cards


@pytest.mark.skipif(
    parse(cards.__version__).major < 2,
    reason="Card < comparison not supported in 1.x",
)
def test_less_than():
    c1 = Card("a task")
    c2 = Card("b task")
    assert c1 < c2
