from sqlalchemy import delete, select
import db

query = delete(db.cookies).where(db.cookies.c.cookie_name == "dark chocolate chip")

result = db.connection.execute(query)
print(result.rowcount)  # rows deleted

s = select([db.cookies]).where(db.cookies.c.cookie_name == "dark chocolate chip")
result = db.connection.execute(s).fetchall()
print(len(result))
