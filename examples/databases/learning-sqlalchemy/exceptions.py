# http://docs.sqlalchemy.org/en/latest/core/exceptions.html
# AttributeError occurs when you attempt to access an attribute that doesn’t exist

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
import db

query = select([db.users.c.username])
results = db.connection.execute(query)

for result in results:
    try:
        # AttributeError: Could not locate column in row for column 'password'
        print(result.password)
    except AttributeError as error:
        print(error)

# IntegrityError occurs when we try to do something that would violate the constraints
# configured on a Column or Table

query = select([db.users.c.username])
result = db.connection.execute(query).fetchall()  # => [(u"cookiemon",)]

query = insert(db.users).values(
    username="cookiemon",
    email_address="damon@cookie.com",
    phone="111-111-1111",
    password="password",
)
try:
    result = db.connection.execute(query)
except IntegrityError as error:
    print(error.orig, error.params)
