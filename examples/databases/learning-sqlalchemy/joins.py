from sqlalchemy import Column, ForeignKey, Integer, String, Table, and_, func, select
import db

columns = [
    db.orders.c.order_id,
    db.users.c.username,
    db.users.c.phone,
    db.cookies.c.cookie_name,
    db.line_items.c.quantity,
    db.line_items.c.extended_cost,
]

cookiemon_orders = (
    select(columns)
    .select_from(db.orders.join(db.users).join(db.line_items).join(db.cookies))
    .where(db.users.c.username == "cookiemon")
)

result = db.connection.execute(cookiemon_orders).fetchall()

for row in result:
    print(row)

# Using outerjoin to select from multiple tables

columns = [db.users.c.username, func.count(db.orders.c.order_id)]

all_orders = select(columns).select_from(db.users.outerjoin(db.orders))
all_orders = all_orders.group_by(db.users.c.username)

result = db.connection.execute(all_orders).fetchall()

for row in result:
    print(row)

# Aliases

employee_table = Table(
    "employee",
    db.metadata,
    Column("id", Integer, primary_key=True),
    Column("manager", None, ForeignKey("employee.id")),
    Column("name", String(255)),
)

manager = employee_table.alias()
stmt = select(
    [employee_table.c.name],
    and_(employee_table.c.manager_id == manager.c.id, manager.c.name == "Fred"),
)
print(stmt)
