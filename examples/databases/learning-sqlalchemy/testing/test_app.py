import unittest
from decimal import Decimal

from .app import get_orders_by_customer
from .db import dal, prep_db


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dal.db_init("sqlite:///:memory:")
        prep_db()

    def test_orders_by_customer_blank(self):
        results = get_orders_by_customer("")
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_shipped(self):
        results = get_orders_by_customer("", True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_notshipped(self):
        results = get_orders_by_customer("", False)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_details(self):
        results = get_orders_by_customer("", details=True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_shipped_details(self):
        results = get_orders_by_customer("", True, True)
        self.assertEqual(results, [])

    def test_orders_by_customer_blank_notshipped_details(self):
        results = get_orders_by_customer("", False, True)
        self.assertEqual(results, [])

    def test_orders_by_customer(self):
        expected_results = [("wlk001", "cookiemon", "111-111-1111")]
        results = get_orders_by_customer("cookiemon")
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_shipped_only(self):
        results = get_orders_by_customer("cookiemon", True)
        self.assertEqual(results, [])

    def test_orders_by_customer_unshipped_only(self):
        expected_results = [("wlk001", "cookiemon", "111-111-1111")]
        results = get_orders_by_customer("cookiemon", False)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_with_details(self):
        expected_results = [
            (
                "wlk001",
                "cookiemon",
                "111-111-1111",
                "dark chocolate chip",
                2,
                Decimal("1.00"),
            ),
            (
                "wlk001",
                "cookiemon",
                "111-111-1111",
                "oatmeal raisin",
                12,
                Decimal("3.00"),
            ),
        ]
        results = get_orders_by_customer("cookiemon", details=True)
        self.assertEqual(results, expected_results)

    def test_orders_by_customer_shipped_only_with_details(self):
        results = get_orders_by_customer("cookiemon", True, True)
        self.assertEqual(results, [])

    def test_orders_by_customer_unshipped_only_details(self):
        expected_results = [
            (
                "wlk001",
                "cookiemon",
                "111-111-1111",
                "dark chocolate chip",
                2,
                Decimal("1.00"),
            ),
            (
                "wlk001",
                "cookiemon",
                "111-111-1111",
                "oatmeal raisin",
                12,
                Decimal("3.00"),
            ),
        ]
        results = get_orders_by_customer("cookiemon", False, True)
        self.assertEqual(results, expected_results)
