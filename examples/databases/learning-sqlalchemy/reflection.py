# https://docs.sqlalchemy.org/en/14/core/reflection.html

from sqlalchemy import ForeignKeyConstraint, MetaData, Table, create_engine, select

engine = create_engine("sqlite:///Chinook.sqlite")

metadata = MetaData()

artist = Table("Artist", metadata, autoload=True, autoload_with=engine)
album = Table("Album", metadata, autoload=True, autoload_with=engine)

album
album.columns.keys()
album.foreign_keys

# how to manually add a relationship:
# album.append_constraint(ForeignKeyConstraint(["ArtistId"], ["artist.ArtistId"]))

# Reflecting the whole database --------------------------------------------------------------------

metadata.reflect(bind=engine)
metadata.tables.keys()

# Query Building with Reflected Objects ------------------------------------------------------------

playlist = metadata.tables["Playlist"]

query = select([playlist]).limit(10)
result = engine.execute(query).fetchall()
