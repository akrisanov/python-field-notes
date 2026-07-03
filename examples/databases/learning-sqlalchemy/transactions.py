from datetime import datetime
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Numeric,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    create_engine,
    CheckConstraint,
)

metadata = MetaData()

# Setting up the transactions environment ----------------------------------------------------------

cookies = Table(
    "cookies",
    metadata,
    Column("cookie_id", Integer(), primary_key=True),
    Column("cookie_name", String(50), index=True),
    Column("cookie_recipe_url", String(255)),
    Column("cookie_sku", String(55)),
    Column("quantity", Integer()),
    Column("unit_cost", Numeric(12, 2)),
    CheckConstraint("quantity >= 0", name="quantity_positive"),
)

users = Table(
    "users",
    metadata,
    Column("user_id", Integer(), primary_key=True),
    Column("username", String(15), nullable=False, unique=True),
    Column("email_address", String(255), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("password", String(25), nullable=False),
    Column("created_on", DateTime(), default=datetime.now),
    Column("updated_on", DateTime(), default=datetime.now, onupdate=datetime.now),
)

orders = Table(
    "orders",
    metadata,
    Column("order_id", Integer()),
    Column("user_id", ForeignKey("users.user_id")),
    Column("shipped", Boolean(), default=False),
)

line_items = Table(
    "line_items",
    metadata,
    Column("line_items_id", Integer(), primary_key=True),
    Column("order_id", ForeignKey("orders.order_id")),
    Column("cookie_id", ForeignKey("cookies.cookie_id")),
    Column("quantity", Integer()),
    Column("extended_cost", Numeric(12, 2)),
)

engine = create_engine("sqlite:///:memory:")
metadata.create_all(engine)
connection = engine.connect()

from sqlalchemy import select, insert, update

query = insert(users).values(
    username="cookiemon",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password",
)
result = connection.execute(query)

query = cookies.insert()
inventory_list = [
    {
        "cookie_name": "chocolate chip",
        "cookie_recipe_url": "http://some.aweso.me/cookie/recipe.html",
        "cookie_sku": "CC01",
        "quantity": "12",
        "unit_cost": "0.50",
    },
    {
        "cookie_name": "dark chocolate chip",
        "cookie_recipe_url": "http://some.aweso.me/cookie/recipe_dark.html",
        "cookie_sku": "CC02",
        "quantity": "1",
        "unit_cost": "0.75",
    },
]
result = connection.execute(query, inventory_list)

# Adding the orders --------------------------------------------------------------------------------

query = insert(orders).values(user_id=1, order_id="1")
result = connection.execute(query)

query = insert(line_items)
order_items = [{"order_id": 1, "cookie_id": 1, "quantity": 9, "extended_cost": 4.50}]
result = connection.execute(query, order_items)

query = insert(orders).values(user_id=1, order_id="2")
result = connection.execute(query)

query = insert(line_items)
order_items = [
    {"order_id": 2, "cookie_id": 1, "quantity": 4, "extended_cost": 1.50},
    {"order_id": 2, "cookie_id": 2, "quantity": 1, "extended_cost": 4.50},
]
result = connection.execute(query, order_items)

# Defining the ship_it function --------------------------------------------------------------------

from sqlalchemy.exc import IntegrityError


def ship_it(order_id):
    """Accept an order_id, remove the cookies from inventory, and mark the order as shipped."""
    s = select([line_items.c.cookie_id, line_items.c.quantity])
    s = s.where(line_items.c.order_id == order_id)

    transaction = connection.begin()

    cookies_to_ship = connection.execute(s).fetchall()

    try:
        for cookie in cookies_to_ship:
            u = update(cookies).where(cookies.c.cookie_id == cookie.cookie_id)
            u = u.values(quantity=cookies.c.quantity - cookie.quantity)
            connection.execute(u)

        u = update(orders).where(orders.c.order_id == order_id)
        u = u.values(shipped=True)
        connection.execute(u)

        print("Shipped order ID: {}".format(order_id))
        transaction.commit()
    except IntegrityError as error:
        transaction.rollback()
        print(error)


ship_it(1)
