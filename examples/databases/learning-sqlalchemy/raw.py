"""Execute raw SQL statements or use raw SQL in part of a SQLAlchemy Core query.
It still returns a ResultProxy."""

from sqlalchemy import select, text
import db

result = db.connection.execute("select * from orders").fetchall()

print(result)  # => [(1, 1, 0), (2, 2, 0)]

stmt = select([db.users]).where(text("username='cookiemon'"))

result = db.connection.execute(stmt).fetchall()

print(result)

# [
#     (
#         None,
#         "cookiemon",
#         "mon@cookie.com",
#         "111-111-1111",
#         "password",
#         datetime.datetime(2022, 1, 11, 23, 3, 41, 962780),
#         datetime.datetime(2022, 1, 11, 23, 3, 41, 962791),
#     )
# ]
