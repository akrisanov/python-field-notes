import pytest
from cards import Card

text_variants = {
    "Short": "x",
    "With Spaces": "x y z",
    "End In Spaces": "x ",
    "Mixed Case": "SuMmArY wItH MiXeD cAsE",
    "Unicode": "¡¢£¤¥¦§ ̈©a«¬® ̄°±23 ́μ¶· ̧1o»1⁄41⁄23⁄4",
    "Newlines": "a\nb\nc",
    "Tabs": "a\tb\tc",
}


@pytest.mark.parametrize("variant", text_variants.values(), ids=text_variants.keys())
def test_summary_variants(db, variant):
    i = db.add_card(Card(summary=variant))
    c = db.get_card(i)
    assert c.summary == variant
