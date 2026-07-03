def test_failing():
    assert (1, 2, 3) == (3, 2, 1)


if __name__ == "__main__":
    # run python test_two.py
    # to see how less information assert without pytest gives us
    test_failing()
