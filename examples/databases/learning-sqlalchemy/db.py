from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
    UniqueConstraint,
    create_engine,
)

sqllite_engine = create_engine("sqlite:///cookies.db")
connection = sqllite_engine.connect()

metadata = MetaData()

cookies = Table(
    "cookies",
    metadata,
    Column("cookie_id", Integer(), primary_key=True),
    Column("cookie_name", String(50), index=True),
    Column("cookie_recipe_url", String(255)),
    Column("cookie_sku", String(55)),
    Column("quantity", Integer()),
    Column("unit_cost", Numeric(12, 2)),
    CheckConstraint("unit_cost >= 0.00", name="unit_cost_positive"),
    # Index("ix_cookies_cookie_name", "cookie_name"),
)

users = Table(
    "users",
    metadata,
    Column("user_id", Integer()),
    Column("username", String(15), nullable=False, unique=True),
    Column("email_address", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("password", String(25), nullable=False),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now),
    # PrimaryKeyConstraint("user_id", name="user_pk"),
    # UniqueConstraint("username", name="uix_username"),
)

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer(), primary_key=True),
    Column("user_id", ForeignKey("users.user_id")),
    Column("shipped", Boolean(), default=False),
)

line_items = Table(
    "line_items",
    metadata,
    Column("line_items_id", Integer(), primary_key=True),
    Column("order_id", ForeignKey("orders.order_id")),
    # another option is defining ForeignKeyConstraint explicitly
    Column("cookie_id", ForeignKey("cookies.cookie_id")),
    Column("quantity", Integer()),
    Column("extended_cost", Numeric(12, 2)),
)

metadata.create_all(sqllite_engine)
