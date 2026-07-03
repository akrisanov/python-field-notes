from sqlalchemy import func, select
import db

columns = [db.users.c.username, func.count(db.orders.c.order_id)]

all_orders = select(columns)
all_orders = all_orders.select_from(db.users.outerjoin(db.orders))
all_orders = all_orders.group_by(db.users.c.username)

result = db.connection.execute(all_orders).fetchall()

for row in result:
    print(row)
