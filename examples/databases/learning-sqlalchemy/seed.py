from sqlalchemy import insert
import db

customer_list = [
    {
        "username": "cookiemon",
        "email_address": "mon@cookie.com",
        "phone": "111-111-1111",
        "password": "password",
    },
    {
        "username": "cakeeater",
        "email_address": "cakeeater@cake.com",
        "phone": "222-222-2222",
        "password": "password",
    },
    {
        "username": "pieguy",
        "email_address": "guy@pie.com",
        "phone": "333-333-3333",
        "password": "password",
    },
]
query = db.users.insert()
result = db.connection.execute(query, customer_list)

query = insert(db.orders).values(user_id=1, order_id=1)
result = db.connection.execute(query)

query = insert(db.line_items)
order_items = [
    {"order_id": 1, "cookie_id": 1, "quantity": 2, "extended_cost": 1.00},
    {"order_id": 1, "cookie_id": 3, "quantity": 12, "extended_cost": 3.00},
]
result = db.connection.execute(query, order_items)

query = insert(db.orders).values(user_id=2, order_id=2)
result = db.connection.execute(query)

query = insert(db.line_items)
order_items = [
    {"order_id": 2, "cookie_id": 1, "quantity": 24, "extended_cost": 12.00},
    {"order_id": 2, "cookie_id": 4, "quantity": 6, "extended_cost": 6.00},
]
result = db.connection.execute(query, order_items)
