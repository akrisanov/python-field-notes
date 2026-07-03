# https://docs.sqlalchemy.org/en/14/orm/extensions/associationproxy.html

from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    String,
    Table,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Base = declarative_base()
Session = sessionmaker(bind=engine)

cookieingredients_table = Table(
    "cookieingredients",
    Base.metadata,
    Column(
        "cookie_id",
        Integer,
        ForeignKey("cookies.cookie_id"),
        primary_key=True,
    ),
    Column(
        "ingredient_id",
        Integer,
        ForeignKey("ingredients.ingredient_id"),
        primary_key=True,
    ),
)


class Ingredient(Base):
    __tablename__ = "ingredients"
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(255), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Ingredient(name='{self.name}')"


class Cookie(Base):
    __tablename__ = "cookies"

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    ingredients = relationship("Ingredient", secondary=cookieingredients_table)

    ingredient_names = association_proxy("ingredients", "name")

    def __repr__(self):
        return (
            f"Cookie(cookie_name='{self.cookie_name}', "
            f"cookie_recipe_url='{self.cookie_recipe_url}', "
            f"cookie_sku='{self.cookie_sku}', "
            f"quantity={self.quantity}, "
            f"unit_cost={self.unit_cost})"
        )


session = Session()

cc_cookie = Cookie(
    cookie_name="chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
    cookie_sku="CC01",
    quantity=12,
    unit_cost=0.50,
)

flour = Ingredient(name="Flour")
sugar = Ingredient(name="Sugar")
egg = Ingredient(name="Egg")
cc = Ingredient(name="Chocolate Chips")

cc_cookie.ingredients.extend([flour, sugar, egg, cc])
session.add(cc_cookie)

dcc = Cookie(
    cookie_name="dark chocolate chip",
    cookie_recipe_url="http://some.aweso.me/cookie/recipe_dark.html",
    cookie_sku="CC02",
    quantity=1,
    unit_cost=0.75,
)
session.add(dcc)
session.flush()

# if we want to list the names of all the ingredients, which was our original goal,
# we have to iterate through all the ingredients and get the name attribute:
[ingredient.name for ingredient in cc_cookie.ingredients]
# vs
cc_cookie.ingredient_names

# When we do this, the association proxy creates a new ingredient using
# the `Ingredient.__init__`` method for us automatically.
cc_cookie.ingredient_names.append("Oil")
session.flush()

# If we already had an ingredient named Oil, the association proxy would
# still attempt to create it for us! Workaround?
dcc_ingredient_list = ["Flour", "Sugar", "Egg", "Dark Chocolate Chips", "Oil"]

existing_ingredients = (
    session.query(Ingredient).filter(Ingredient.name.in_(dcc_ingredient_list)).all()
)
missing = set(dcc_ingredient_list) - set([x.name for x in existing_ingredients])
dcc.ingredients.extend(existing_ingredients)
dcc.ingredient_names.extend(missing)
dcc.ingredient_names
