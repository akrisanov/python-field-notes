from sqlalchemy import select, update
import db

query = update(db.cookies).where(db.cookies.c.cookie_name == "chocolate chip")
query = query.values(quantity=(db.cookies.c.quantity + 120))

result = db.connection.execute(query)
print(result.rowcount)

query = select([db.cookies]).where(db.cookies.c.cookie_name == "chocolate chip")
result = db.connection.execute(query).first()

for key in result.keys():
    print("{:>20}: {}".format(key, result[key]))
