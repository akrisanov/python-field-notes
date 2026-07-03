from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cookie(Base):
    __tablename__ = "cookies"
    __table_args__ = (CheckConstraint("quantity >= 0", name="quantity_positive"),)

    cookie_id = Column(Integer(), primary_key=True)  # at least one primary key field
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def __init__(self, name, recipe_url=None, sku=None, quantity=0, unit_cost=0.00):
        self.cookie_name = name
        self.cookie_recipe_url = recipe_url
        self.cookie_sku = sku
        self.quantity = quantity
        self.unit_cost = unit_cost

    def __repr__(self):
        return (
            f"Cookie(cookie_name='{self.cookie_name}', "
            f"cookie_recipe_url='{self.cookie_recipe_url}', "
            f"cookie_sku='{self.cookie_sku}', "
            f"quantity={self.quantity}, "
            f"unit_cost={self.unit_cost})"
        )


Cookie.__table__  # => table metadata/definition


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, email_address, phone, password):
        self.username = username
        self.email_address = email_address
        self.phone = phone
        self.password = password

    def __repr__(self):
        return (
            f"User(username='{self.username}', "
            f"email_address='{self.email_address}', "
            f"phone='{self.phone}', "
            f"password='{self.password}')"
        )


# Relationships ------------------------------------------------------------------------------------

from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.user_id"))
    shipped = Column(Boolean(), default=False)

    user = relationship(
        "User", backref=backref("orders", order_by=order_id)
    )  # one-to-many

    def __repr__(self):
        return f"Order(user_id={self.user_id}, " "shipped={self.shipped})"


class LineItem(Base):
    __tablename__ = "line_items"

    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey("orders.order_id"))
    cookie_id = Column(Integer(), ForeignKey("cookies.cookie_id"))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))

    order = relationship("Order", backref=backref("line_items", order_by=line_item_id))
    cookie = relationship("Cookie", uselist=False)  # one-to-one

    def __repr__(self):
        return (
            f"LineItems(order_id={self.order_id}, "
            f"cookie_id={self.cookie_id}, "
            f"quantity={self.quantity}, "
            f"extended_cost={self.extended_cost})"
        )


# Keys, Constraints, and Indexes -------------------------------------------------------------------

# from sqlalchemy import CheckConstraint, ForeignKeyConstraint


# class SomeDataClass(Base):
#     __tablename__ = "somedatatable"
#     __table_args__ = (
#         ForeignKeyConstraint(["id"], ["other_table.id"]),
#         CheckConstraint("unit_cost >= 0.00", name="unit_cost_positive"),
#     )

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)  # create all the tables

# The session is the way SQLAlchemy ORM interacts with the database.
# It wraps a database connection via an engine, and provides an identity map for objects that you
# load via the session or associate with the session.

Session = sessionmaker(bind=engine)
session = Session()

# While session has everything it needs to connect to the database, it won’t connect until we give
# it some instructions that require it to do so.

cc_cookie = Cookie(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity=12,
    unit_cost=0.50,
)
session.add(cc_cookie)
session.commit()

print(cc_cookie.cookie_id)

dcc = Cookie(
    cookie_name="dark chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe_dark.html",
    cookie_sku="CC02",
    quantity=1,
    unit_cost=0.75,
)
mol = Cookie(
    cookie_name="molasses",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe_molasses.html",
    cookie_sku="MOL01",
    quantity=1,
    unit_cost=0.80,
)
session.add(dcc)
session.add(mol)
session.flush()

# A flush is like a commit; however, it doesn’t perform a database commit and end the transaction.
# https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit

print(dcc.cookie_id)
print(mol.cookie_id)

# https://docs.sqlalchemy.org/en/14/orm/persistence_techniques.html#bulk-operations
# Bulk saves substantially faster than performing multiple individual adds and inserts, but
# • Relationship settings and actions are not respected or triggered.
# • The objects are not connected to the session.
# • Fetching primary keys is not done by default.
# • No events will be triggered.

c1 = Cookie(
    cookie_name="peanut butter",
    cookie_recipe_url="http://some.aweso.me/cookie/peanut.html",
    cookie_sku="PB01",
    quantity=24,
    unit_cost=0.25,
)
c2 = Cookie(
    cookie_name="oatmeal raisin",
    cookie_recipe_url="http://some.okay.me/cookie/raisin.html",
    cookie_sku="EWW01",
    quantity=100,
    unit_cost=1.00,
)
session.bulk_save_objects([c1, c2])
session.commit()

print(c1.cookie_id)

# Querying data ------------------------------------------------------------------------------------

cookies = session.query(Cookie).all()

# Using the iterable approach allows us to interact with each record object individually,
# release it, and get the next object → no need to call .all():
for cookie in session.query(Cookie):
    print(cookie)

# Controlling the Columns in the Query -------------------------------------------------------------

session.query(
    Cookie.cookie_name,
    Cookie.quantity,
).first()

# Ordering -----------------------------------------------------------------------------------------

for cookie in session.query(Cookie).order_by(Cookie.quantity):
    print("{:3} - {}".format(cookie.quantity, cookie.cookie_name))

# Order by quantity descending
from sqlalchemy import desc

for cookie in session.query(Cookie).order_by(desc(Cookie.quantity)):
    print("{:3} - {}".format(cookie.quantity, cookie.cookie_name))

# Limiting -----------------------------------------------------------------------------------------

query = session.query(Cookie).order_by(Cookie.quantity).limit(2)

# Built-In SQL Functions and Labels ----------------------------------------------------------------

from sqlalchemy import func

inv_count = session.query(func.sum(Cookie.quantity)).scalar()
rec_count = session.query(
    func.count(Cookie.cookie_name).label("inventory_count")
).first()

rec_count.keys()  # => ["inventory_count"]
rec_count.inventory_count  # => 5

# Filtering ----------------------------------------------------------------------------------------

record = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").first()
record = session.query(Cookie).filter_by(cookie_name="chocolate chip").first()
query = session.query(Cookie).filter(
    Cookie.cookie_name.like("%chocolate%")
)  # ClauseElement

for record in query:
    print(record.cookie_name)

# Operators

results = session.query(Cookie.cookie_name, "SKU-" + Cookie.cookie_sku).all()

# common usage of operators is to compute values from multiple columns
from sqlalchemy import cast

query = session.query(
    Cookie.cookie_name,
    cast((Cookie.quantity * Cookie.unit_cost), Numeric(12, 2)).label("inv_cost"),
)

# Conjunctions

query = session.query(Cookie).filter(Cookie.quantity > 23, Cookie.unit_cost < 0.40)

from sqlalchemy import and_, or_, not_

query = session.query(Cookie).filter(
    or_(
        Cookie.quantity.between(10, 50),
        Cookie.cookie_name.contains("chip"),
    )
)

# Updating Data ------------------------------------------------------------------------------------

cc_cookie = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").first()
cc_cookie.quantity = cc_cookie.quantity + 120
session.commit()

print(cc_cookie.quantity)  # => 132

# It is also possible to update data in place without having the object originally:
query = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip")
query.update({Cookie.quantity: Cookie.quantity - 20})
cc_cookie = query.first()
print(cc_cookie.quantity)  # => 112

# Deleting Data ------------------------------------------------------------------------------------

query = session.query(Cookie).filter(Cookie.cookie_name == "dark chocolate chip")
dcc_cookie = query.one()
session.delete(dcc_cookie)
session.commit()
dcc_cookie = query.first()
print(dcc_cookie)

# It is also possible to delete data in place without having the object:
query = session.query(Cookie).filter(Cookie.cookie_name == "molasses")
query.delete()
mol_cookie = query.first()
print(mol_cookie)  # => None

# --------------------------------------------------------------------------------------------------

cookiemon = User(
    username="cookiemon",
    email_address="mon@cookie.com",
    phone="111-111-1111",
    password="password",
)
cakeeater = User(
    username="cakeeater",
    email_address="cakeeater@cake.com",
    phone="222-222-2222",
    password="password",
)
pieperson = User(
    username="pieperson",
    email_address="person@pie.com",
    phone="333-333-3333",
    password="password",
)
session.add(cookiemon)
session.add(cakeeater)
session.add(pieperson)
session.commit()

o1 = Order()
o1.user = cookiemon
session.add(o1)

cc = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").one()
line1 = LineItem(cookie=cc, quantity=2, extended_cost=1.00)

pb = session.query(Cookie).filter(Cookie.cookie_name == "peanut butter").one()
line2 = LineItem(quantity=12, extended_cost=3.00)
line2.cookie = pb
line2.order = o1

o1.line_items.append(line1)
o1.line_items.append(line2)

session.commit()

o2 = Order()
o2.user = cakeeater

cc = session.query(Cookie).filter(Cookie.cookie_name == "chocolate chip").one()

line1 = LineItem(cookie=cc, quantity=24, extended_cost=12.00)
oat = session.query(Cookie).filter(Cookie.cookie_name == "oatmeal raisin").one()

line2 = LineItem(cookie=oat, quantity=6, extended_cost=6.00)
o2.line_items.append(line1)
o2.line_items.append(line2)

session.add(o2)
session.commit()

# Joins --------------------------------------------------------------------------------------------

session.query(
    Order.order_id,
    User.username,
    User.phone,
    Cookie.cookie_name,
    LineItem.quantity,
    LineItem.extended_cost,
).join(User).join(LineItem).join(Cookie).filter(User.username == "cookiemon").all()

session.query(User.username, func.count(Order.order_id)).outerjoin(Order).group_by(
    User.username
)

# Self-reference -----------------------------------------------------------------------------------


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer(), primary_key=True)
    manager_id = Column(Integer(), ForeignKey("employees.id"))
    name = Column(String(255), nullable=False)
    # we need to specify an option called remote_side to make the relationship a many to one:
    manager = relationship("Employee", backref=backref("reports"), remote_side=[id])


marsha = Employee(name="Marsha")
fred = Employee(name="Fred")
marsha.reports.append(fred)
session.add(marsha)
session.commit()

for report in marsha.reports:
    print(report.name)


# Grouping -----------------------------------------------------------------------------------------

query = session.query(User.username, func.count(Order.order_id))
query = query.outerjoin(Order).group_by(User.username)

for row in query:
    print(row)

# ("cakeeater", 1)
# ("cookiemon", 1)
# ("pieguy", 0)

# Chaining -----------------------------------------------------------------------------------------


def get_orders_by_customer(cust_name, shipped=None, details=False):
    query = session.query(Order.order_id, User.username, User.phone).join(User)
    if details:
        columns = (Cookie.cookie_name, LineItem.quantity, LineItem.extended_cost)
        query = query.add_columns(*columns)
        query = query.join(LineItem).join(Cookie)
    if shipped is not None:
        query = query.where(Order.shipped == shipped)
    results = query.filter(User.username == cust_name).all()
    return results


get_orders_by_customer("cakeeater")
get_orders_by_customer("cakeeater", details=True)
get_orders_by_customer("cakeeater", shipped=True)
get_orders_by_customer("cakeeater", shipped=False)
get_orders_by_customer("cakeeater", shipped=False, details=True)

# Raw Queries --------------------------------------------------------------------------------------

from sqlalchemy import text

query = session.query(User).filter(text("username='cookiemon'"))
result = query.all()

# The Session and introspection --------------------------------------------------------------------

from sqlalchemy import inspect

cc_cookie = Cookie(
    "chocolate chip", "http://some.aweso.me/cookie/recipe.html", "CC01", 12, 0.50
)

insp = inspect(cc_cookie)

insp.transient
insp.pending
insp.persistent
insp.detached

for state in ["transient", "pending", "persistent", "detached"]:
    print("{:>10}: {}".format(state, getattr(insp, state)))

#   transient: True ← state newly created objects are in prior to being flushed or commited to db
#    pending: False
# persistent: False
#   detached: False

session.add(cc_cookie)
cc_cookie.cookie_name = "Change chocolate chip"
insp.modified  # => True

# Printing the changed attribute history:
for attr, attr_state in insp.attrs.items():
    if attr_state.history.has_changes():
        print(f"{attr}: {attr_state.value}")
        print("History: {attr_state.history}\n")

# cookie_name: Change chocolate chip
# History: History(added=['Change chocolate chip'], unchanged=(), deleted=())

# Exceptions ---------------------------------------------------------------------------------------

# MultipleResultsFound Exception

dcc = Cookie(
    "dark chocolate chip",
    "http://some.aweso.me/cookie/recipe_dark.html",
    "CC02",
    1,
    0.75,
)
session.add(dcc)
session.commit()

from sqlalchemy.orm.exc import MultipleResultsFound

try:
    results = session.query(Cookie).one()
except MultipleResultsFound as error:
    print("We found too many cookies... is that even possible?")

# DetachedInstanceError

cookiemon = User("cookiemon", "mon@cookie.com", "111-111-1111", "password")
session.add(cookiemon)

o1 = Order()
o1.user = cookiemon
session.add(o1)

cc = session.query(Cookie).filter(Cookie.cookie_name == "Change chocolate chip").one()
line1 = LineItem(order=o1, cookie=cc, quantity=2, extended_cost=1.00)
session.add(line1)
session.commit()

order = session.query(Order).first()
session.expunge(order)  # detach the row instance from the session
order.line_items  # exception!

# Transactions -------------------------------------------------------------------------------------

cookiemon = User("cookiemon", "mon@cookie.com", "111-111-1111", "password")
cc = Cookie(
    "chocolate chip",
    "http://some.aweso.me/cookie/recipe.html",
    "CC01",
    12,
    0.50,
)
dcc = Cookie(
    "dark chocolate chip",
    "http://some.aweso.me/cookie/recipe_dark.html",
    "CC02",
    1,
    0.75,
)
session.add(cookiemon)
session.add(cc)
session.add(dcc)

o1 = Order()
o1.user = cookiemon
session.add(o1)

line1 = LineItem(order=o1, cookie=cc, quantity=9, extended_cost=4.50)
session.add(line1)
session.commit()

o2 = Order()
o2.user = cookiemon
session.add(o2)

line1 = LineItem(order=o2, cookie=cc, quantity=2, extended_cost=1.50)
line2 = LineItem(order=o2, cookie=dcc, quantity=9, extended_cost=6.75)
session.add(line1)
session.add(line2)

session.commit()

from sqlalchemy.exc import IntegrityError


def ship_it(order_id):
    order = session.query(Order).get(order_id)

    for li in order.line_items:
        li.cookie.quantity = li.cookie.quantity - li.quantity
        session.add(li.cookie)

    order.shipped = True
    session.add(order)

    try:
        session.commit()
        print("shipped order ID: {}".format(order_id))
    except IntegrityError as error:
        print("ERROR: {!s}".format(error.orig))
        session.rollback()
