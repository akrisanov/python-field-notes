import unittest
from unittest import mock
from decimal import Decimal

from . import app, db


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.dal.db_init("sqlite:///:memory:")
        db.prep_db()

    cookie_orders = [("wlk001", "cookiemon", "111-111-1111")]
    cookie_details = [
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

    @mock.patch("app.select")
    @mock.patch("app.dal.connection")
    def test_orders_by_customer_blank(self, mock_conn, mock_select):
        mock_select.return_value.select_from.return_value.where.return_value = None
        mock_conn.execute.return_value.fetchall.return_value = []
        results = app.get_orders_by_customer("")
        self.assertEqual(results, [])

    @mock.patch("app.dal.connection")
    def test_orders_by_customer_blank_shipped(self, mock_conn):
        mock_conn.execute.return_value.fetchall.return_value = []
        results = app.get_orders_by_customer("", True)
        self.assertEqual(results, [])

    @mock.patch("app.dal.connection")
    def test_orders_by_customer(self, mock_conn):
        mock_conn.execute.return_value.fetchall.return_value = self.cookie_orders
        results = app.get_orders_by_customer("cookiemon")
        self.assertEqual(results, self.cookie_orders)
