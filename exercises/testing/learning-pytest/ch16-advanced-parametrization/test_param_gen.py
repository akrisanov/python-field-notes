import pytest
from cards import Card


def text_variants():
    """Parametrizing with Dynamic Values."""
    variants = {
        "Short": "x",
        "With Spaces": "x y z",
        "End in Spaces": "x ",
        "Mixed Case": "SuMmArY wItH MiXeD cAsE",
        "Unicode": "¡¢£¤¥¦§ ̈©a«¬® ̄°±23 ́μ¶· ̧1o»1⁄41⁄23⁄4",
        "Newlines": "a\nb\nc",
        "Tabs": "a\tb\tc",
    }
    for key, value in variants.items():
        yield pytest.param(value, id=key)


@pytest.mark.parametrize("variant", text_variants())
def test_summary(db, variant):
    i = db.add_card(Card(summary=variant))
    c = db.get_card(i)
    assert c.summary == variant
