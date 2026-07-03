from sqlalchemy import select
import db


def get_orders_by_customer(cust_name, shipped=None, details=False):
    columns = [db.orders.c.order_id, db.users.c.username, db.users.c.phone]
    joins = db.users.join(db.orders)
    if details:
        columns.extend(
            [
                db.cookies.c.cookie_name,
                db.line_items.c.quantity,
                db.line_items.c.extended_cost,
            ]
        )
        joins = joins.join(db.line_items).join(db.cookies)
    cust_orders = select(columns).select_from(joins)
    cust_orders = cust_orders.where(db.users.c.username == cust_name)
    if shipped is not None:
        cust_orders = cust_orders.where(db.orders.c.shipped == shipped)

    result = db.connection.execute(cust_orders).fetchall()
    return result


get_orders_by_customer("cakeeater")
get_orders_by_customer("cakeeater", details=True)
get_orders_by_customer("cakeeater", shipped=True)
get_orders_by_customer("cakeeater", shipped=False)
get_orders_by_customer("cakeeater", shipped=False, details=True)
