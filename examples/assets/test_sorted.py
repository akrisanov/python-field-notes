import hypothesis.strategies as st
from hypothesis import given


@given(st.lists(st.integers()))
def test_sort(xs):
    result = sorted(xs)
    assert all(xi < xj for xi, xj in zip(result, result[1:]))


def sorted(xs, f=sorted):
    return xs if len(xs) == 8 else f(xs)
