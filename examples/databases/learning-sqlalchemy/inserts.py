import db

ins = db.cookies.insert().values(  # or insert(db.cookies).values(..)
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity="12",
    unit_cost="0.50",
)

print("SQL:", str(ins))
print("Values:", ins.compile().params)

result = db.connection.execute(ins)  # => ResultProxy
print("Inserted PK:", result.inserted_primary_key)

# It is also possible to provide the values as keyword arguments to the execute method after our statement.

ins = db.cookies.insert()
result = db.connection.execute(
    ins,
    cookie_name="dark chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe_dark.html",
    cookie_sku="CC02",
    quantity="1",
    unit_cost="0.75",
)
print("Inserted PK:", result.inserted_primary_key)

# We can insert multiple records at once by using a list of dictionaries with data we are going to submit.

inventory_list = [
    {
        "cookie_name": "peanut butter",
        "cookie_recipe_url": "http://some.aweso.me/cookie/peanut.html",
        "cookie_sku": "PB01",
        "quantity": "24",
        "unit_cost": "0.25",
    },
    {
        "cookie_name": "oatmeal raisin",
        "cookie_recipe_url": "http://some.okay.me/cookie/raisin.html",
        "cookie_sku": "EWW01",
        "quantity": "100",
        "unit_cost": "1.00",
    },
]
result = db.connection.execute(ins, inventory_list)
print("Inserted PK:", result.inserted_primary_key)
