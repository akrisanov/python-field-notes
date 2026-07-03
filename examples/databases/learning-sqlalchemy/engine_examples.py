from sqlalchemy import create_engine

sqllite_engine = create_engine("sqllite:///cookies.db")
inmemory_engine = create_engine("sqlite:///:memory:")
postres_engine = create_engine(
    "postgresql+psycopg2://akrisanov:password00@localhost:5432/exchange_dev",
    pool_recycle=3600,
)

connection = postres_engine.connect()
