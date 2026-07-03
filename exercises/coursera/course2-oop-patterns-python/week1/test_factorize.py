import unittest


def factorize(x):
    """
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    """
    pass


class TestFactorize(unittest.TestCase):
    def _assertCases(self, cases):
        for x, expected in cases:
            with self.subTest(x=x):
                self.assertEqual(factorize(x), expected)

    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1, -10, -100)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = (
            (0, (0,)),
            (1, (1,)),
        )
        self._assertCases(cases)

    def test_simple_numbers(self):
        cases = (
            (3, (3,)),
            (13, (13,)),
            (29, (29,)),
        )
        self._assertCases(cases)

    def test_two_simple_multipliers(self):
        cases = (
            (6, (2, 3)),
            (26, (2, 13)),
            (121, (11, 11)),
        )
        self._assertCases(cases)

    def test_many_multipliers(self):
        cases = (
            (1001, (7, 11, 13)),
            (9699690, (2, 3, 5, 7, 11, 13, 17, 19)),
        )
        self._assertCases(cases)
